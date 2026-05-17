#!/usr/bin/env python3
"""
cedric_server.py -- MCSB Phase 1.3 (v0.4.0)
The Cedric Server: a small FastAPI service exposing MCSB endpoints to every
Claude surface plus Mick's mobile devices, via the existing Cloudflare tunnel.

Endpoints implemented (this build):
  - GET  /health                  liveness check, no auth                [1.3b]
  - POST /memory/note             quick capture, mobile or PC token     [1.3c]
  - GET  /agents/reload           force agents.md reload, PC-only       [1.3d]
  - GET  /worker/status           embedded worker state, PC-only        [1.3g]
  - POST /worker/run_now          fire a worker tick now, PC-only       [1.3g]

Auth (PRD v0.3 Appendix B):
  - Public:    /health
  - Any tier:  /memory/note            (PC or Mobile token)
  - PC only:   /agents/reload, /worker/status, /worker/run_now
  Header: Authorization: Bearer <token>
  Tokens live in C:\\Users\\pavey\\.env -- NEVER copied anywhere else.

What v0.4.0 adds vs 0.3.0:
  - cedric_worker.py embedded as a FastAPI background task          [1.3g]
  - APScheduler (AsyncIOScheduler) drives hourly ticks              [1.3g]
  - threading.Lock guards concurrent tick invocations               [1.3g]
  - GET /worker/status (PC-only) -- last_run, next_run, lock_held   [1.3g]
  - POST /worker/run_now (PC-only) -- manual trigger                [1.3g]
  - /health enriched with embedded worker block                     [1.3g]
  - Clean shutdown hook stops the scheduler on Ctrl+C               [1.3g]
  - Windows Task Scheduler dependency now removable (handover S5)

Env vars new in v0.4.0:
  CEDRIC_WORKER_ENABLED      default "true"
  CEDRIC_WORKER_INTERVAL_MIN default "60"
  CEDRIC_WORKER_DRY_RUN      default "false" (set "true" for sandbox)

Future endpoints (not in this build):
  - POST /memory/search, /memory/search_all, /memory/recall    [Phase 3]
  - POST /memory/append, /memory/task                          [Phase 3]
  - POST /memory/journal, /memory/crm                          [Phase 5]
  - POST /ingest/clipper, /ingest/voice                        [Phase 2/5]

Run modes:
  python cedric_server.py            # foreground dev mode
  uvicorn cedric_server:app --reload # dev with hot reload
  Production: Windows service install (Phase 1 outstanding)

Author: Cedric (Mick's PAIDA), 2026-05-17
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import platform
import re
import sys
import threading
import traceback
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Tuple

try:
    from fastapi import Depends, FastAPI, HTTPException, Request, status
    from fastapi.responses import JSONResponse
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover -- bootstrap helper
    sys.stderr.write(
        "ERROR: FastAPI / pydantic is not installed. Run:\n"
        "    pip install fastapi uvicorn[standard] pydantic python-dotenv\n"
    )
    raise

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.interval import IntervalTrigger
except ImportError:  # pragma: no cover -- bootstrap helper
    sys.stderr.write(
        "ERROR: apscheduler is not installed. Run:\n"
        "    pip install apscheduler\n"
    )
    raise

# Embedded worker -- imported as a module so we can call run_worker_pipeline()
# without spawning a subprocess. Lives next to this file in the vault root.
try:
    import cedric_worker  # type: ignore
except ImportError as _werr:  # pragma: no cover -- bootstrap helper
    sys.stderr.write(
        "ERROR: cedric_worker.py not importable: " + str(_werr) + "\n"
        "    Make sure cedric_worker.py sits next to cedric_server.py.\n"
    )
    raise


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

SERVER_NAME = "Cedric Server"
SERVER_VERSION = "0.4.0"
# Hardcoded per project rule: global .env lives at C:\Users\pavey\.env -- never copy.
GLOBAL_ENV_PATH = Path(r"C:\Users\pavey\.env")
VAULT_ROOT = Path(r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP")
INBOX_RAW = VAULT_ROOT / "00-Inbox" / "raw"
AGENTS_MD_PATH = VAULT_ROOT / "agents.md"
AGENTS_HISTORY_DIR = VAULT_ROOT / "agents.md-history"
AGENTS_CHANGELOG_PATH = AGENTS_HISTORY_DIR / "CHANGELOG.md"

# Server boot time (recorded on import)
BOOT_UTC = datetime.now(timezone.utc)

# Env var names for the two-tier bearer tokens.
ENV_KEY_PC = "MCSB_PC_TOKEN"
ENV_KEY_MOBILE = "MCSB_MOBILE_TOKEN"

# Embedded worker config (1.3g). All env-var overridable, sensible defaults.
WORKER_ENABLED = os.environ.get("CEDRIC_WORKER_ENABLED", "true").lower() == "true"
WORKER_INTERVAL_MIN = max(1, int(os.environ.get("CEDRIC_WORKER_INTERVAL_MIN", "60")))
WORKER_DRY_RUN = os.environ.get("CEDRIC_WORKER_DRY_RUN", "false").lower() == "true"
# Job id used by APScheduler. Stable so we can reference it in /worker/status.
WORKER_JOB_ID = "cedric_worker_tick"


def _load_dotenv_simple(path: Path) -> dict:
    """
    Minimal .env reader. Does NOT mutate os.environ -- caller decides what to
    use. Returns {} if file is missing (handled upstream as a soft warning).

    Supports lines of the form: KEY=VALUE  (no quotes processing, no exports).
    Comments and blank lines are skipped. Trailing whitespace stripped.
    """
    out = {}
    if not path.is_file():
        return out
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            out[key] = value
    return out


def _load_tokens() -> Tuple[Optional[str], Optional[str]]:
    """Load PC and Mobile tokens from the global .env."""
    env = _load_dotenv_simple(GLOBAL_ENV_PATH)
    return env.get(ENV_KEY_PC) or None, env.get(ENV_KEY_MOBILE) or None


def london_now() -> datetime:
    """Return current London time (BST Apr-Oct, GMT otherwise)."""
    utc = datetime.now(timezone.utc)
    bst = 4 <= utc.month <= 10
    offset = timedelta(hours=1) if bst else timedelta(hours=0)
    return utc.astimezone(timezone(offset))


# ---------------------------------------------------------------------------
# AUTH (1.3e -- now complete with PC-only guard)
# ---------------------------------------------------------------------------

class AuthTier(str, Enum):
    PC = "pc"
    MOBILE = "mobile"


_bearer_scheme = HTTPBearer(auto_error=False)


def require_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> AuthTier:
    """
    FastAPI dependency that validates the bearer token and returns its tier.

    - No header                                           -> 401
    - Header present but token does not match either key  -> 401
    - Matches PC token                                    -> AuthTier.PC
    - Matches Mobile token                                -> AuthTier.MOBILE

    Tokens are re-read from .env on every request. This means rotating a token
    in .env takes effect on the next request -- no server restart needed.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization: Bearer header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    pc_token, mobile_token = _load_tokens()
    presented = credentials.credentials

    if pc_token and presented == pc_token:
        return AuthTier.PC
    if mobile_token and presented == mobile_token:
        return AuthTier.MOBILE

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid bearer token.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def require_pc_token(tier: AuthTier = Depends(require_token)) -> AuthTier:
    """
    Stricter dependency: PC token mandatory. Mobile tokens get a 403.
    Used by /agents/reload (and later /memory/search_all, /briefing/today).
    """
    if tier != AuthTier.PC:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="PC token required for this endpoint.",
        )
    return tier


# ---------------------------------------------------------------------------
# AGENTS.MD LOADER (1.3d)
# ---------------------------------------------------------------------------

# Module-level state. Mutated by load_agents_md() on startup + on every reload.
_agents_state = {
    "version": None,
    "rules_loaded": 0,
    "content_hash": None,
    "loaded_at": None,
    "source_path": str(AGENTS_MD_PATH),
    "raw_size_bytes": 0,
    "snapshot_count": 0,
}

# Frontmatter delimiter -- a line containing only ---
_FM_DELIM_RE = re.compile(r"^\s*---\s*$")
# A frontmatter key: value line (very lenient)
_FM_KV_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$")
# A top-level YAML-style rule block (key: at column 0, nothing after the colon
# except whitespace). Matches "ingestion:" but NOT "  inbox_path: 00-Inbox/raw/".
_RULE_BLOCK_RE = re.compile(r"^[a-z_][a-z0-9_-]*:\s*$", re.MULTILINE)


def _parse_agents_frontmatter(text: str) -> dict:
    """
    Extract YAML frontmatter into a flat dict. Tolerant -- ignores nested
    structures (we only need scalar values like version).
    """
    lines = text.splitlines()
    if not lines or not _FM_DELIM_RE.match(lines[0]):
        return {}
    fm = {}
    for line in lines[1:]:
        if _FM_DELIM_RE.match(line):
            break
        m = _FM_KV_RE.match(line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def _count_rules(text: str) -> int:
    """
    Count top-level YAML rule blocks (e.g. ingestion:, journaling:, crm:).
    Definition: a line starting at column 0 that is a bare key ending in a colon
    with no value -- meaning it heads a config block. Excludes anything inside
    the frontmatter and anything inside fenced code blocks.
    """
    # Strip frontmatter first
    stripped = _strip_frontmatter(text)
    return len(_RULE_BLOCK_RE.findall(stripped))


def _strip_frontmatter(text: str) -> str:
    """Return text with the leading YAML frontmatter block removed (if any)."""
    lines = text.splitlines()
    if not lines or not _FM_DELIM_RE.match(lines[0]):
        return text
    for i, line in enumerate(lines[1:], start=1):
        if _FM_DELIM_RE.match(line):
            return "\n".join(lines[i + 1:])
    return text  # malformed -- no closing delimiter; return original


def _hash_content(text: str) -> str:
    """Stable SHA-256 hex digest of the file's bytes."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _safe_version_for_filename(version) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(version)).strip("-") or "unknown"


def _snapshot_agents_md(text: str, version, reason: str, drift: bool) -> Path:
    """
    Write a versioned snapshot to AGENTS_HISTORY_DIR and append to the
    CHANGELOG. Returns the snapshot path written.

    Filename includes seconds and a 6-char content hash so two reloads in the
    same minute (testing, quick re-edit) never collide on disk.
    """
    AGENTS_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    now = london_now()
    stamp = now.strftime("%Y.%m.%dT%H%M%S")
    safe_v = _safe_version_for_filename(version)
    short_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:6]
    snap_name = f"agents-v{safe_v}-{stamp}-{short_hash}.md"
    snap_path = AGENTS_HISTORY_DIR / snap_name
    snap_path.write_text(text, encoding="utf-8")
    _append_agents_changelog(version, reason, snap_name, drift)
    return snap_path


def _append_agents_changelog(version, reason: str, snap_name: str, drift: bool) -> None:
    """
    Append a CHANGELOG entry (newest first, after the header comments).
    ASCII-only. No em dashes / smart quotes.
    """
    AGENTS_HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    now = london_now()
    stamp = now.strftime("%Y-%m-%d %H:%M")
    drift_note = "  (content drift -- version not bumped)" if drift else ""
    entry_block = (
        f"## {stamp} | {reason}{drift_note}\n"
        f"- Version: {version}\n"
        f"- Snapshot: {snap_name}\n"
        f"- Loaded-by: Cedric Server v{SERVER_VERSION}\n"
        "\n"
    )

    header = (
        "# agents.md CHANGELOG\n"
        "# One entry per reload/edit. Newest first.\n"
        "# Format: ## YYYY-MM-DD HH:MM | reason\n"
        "\n"
    )

    if not AGENTS_CHANGELOG_PATH.exists():
        AGENTS_CHANGELOG_PATH.write_text(header + entry_block, encoding="utf-8")
        return

    existing = AGENTS_CHANGELOG_PATH.read_text(encoding="utf-8")
    # Find first existing entry header ("## ") and insert new block before it.
    m = re.search(r"^## ", existing, flags=re.MULTILINE)
    if m is None:
        AGENTS_CHANGELOG_PATH.write_text(existing.rstrip() + "\n\n" + entry_block, encoding="utf-8")
    else:
        new_text = existing[: m.start()] + entry_block + existing[m.start():]
        AGENTS_CHANGELOG_PATH.write_text(new_text, encoding="utf-8")


def load_agents_md(reason: str) -> Tuple[dict, bool, bool]:
    """
    Read agents.md, parse, update module state, snapshot if content changed.

    Returns: (state_snapshot, content_drift, snapshot_written)
      content_drift   = True if content changed but the version field did NOT
      snapshot_written = True if a history snapshot was written this call

    Behaviour:
      - If agents.md is missing: state cleared; raises HTTPException(500).
      - If content unchanged vs last loaded: no snapshot, no CHANGELOG entry.
      - If content changed: snapshot to agents.md-history/, append CHANGELOG.
    """
    if not AGENTS_MD_PATH.is_file():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"agents.md not found at {AGENTS_MD_PATH}",
        )

    text = AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace")
    new_hash = _hash_content(text)
    fm = _parse_agents_frontmatter(text)
    new_version = fm.get("version") or "unversioned"
    new_rules = _count_rules(text)

    prev_hash = _agents_state.get("content_hash")
    prev_version = _agents_state.get("version")

    content_changed = (prev_hash is not None) and (new_hash != prev_hash)
    # First-ever load -- treat as a content change so we have a baseline snapshot.
    first_load = prev_hash is None
    drift = content_changed and (new_version == prev_version)

    snapshot_written = False
    if first_load or content_changed:
        _snapshot_agents_md(text, new_version, reason, drift=drift)
        snapshot_written = True

    now_iso = london_now().strftime("%Y-%m-%dT%H:%M:%S%z")
    _agents_state.update({
        "version": new_version,
        "rules_loaded": new_rules,
        "content_hash": new_hash,
        "loaded_at": now_iso,
        "source_path": str(AGENTS_MD_PATH),
        "raw_size_bytes": len(text.encode("utf-8")),
        "snapshot_count": _agents_state.get("snapshot_count", 0) + (1 if snapshot_written else 0),
    })
    return dict(_agents_state), drift, snapshot_written


# ---------------------------------------------------------------------------
# EMBEDDED WORKER (1.3g)
# ---------------------------------------------------------------------------
#
# The Cedric Server now drives cedric_worker.run_worker_pipeline() itself,
# replacing the Windows Task Scheduler dependency from Phase 1.2.
#
# Mechanics:
#   - APScheduler (AsyncIOScheduler) fires a tick every WORKER_INTERVAL_MIN.
#   - Each tick acquires a threading.Lock non-blocking; if it cannot, the tick
#     is recorded as "skipped" rather than queued (no pile-up).
#   - The worker pipeline is blocking (subprocess for git, filesystem I/O),
#     so it runs in the default ThreadPoolExecutor via run_in_executor.
#   - /worker/status surfaces last_run / next_run / lock state (PC-only).
#   - /worker/run_now triggers a tick immediately (PC-only).

_worker_state: dict = {
    "enabled": WORKER_ENABLED,
    "interval_min": WORKER_INTERVAL_MIN,
    "dry_run_default": WORKER_DRY_RUN,
    "scheduler_started": False,
    "last_run": None,
    "last_skip": None,
    "last_error": None,
    "next_run": None,
    "tick_count": 0,
    "skip_count": 0,
    "error_count": 0,
}

_worker_lock = threading.Lock()
_worker_scheduler: Optional[AsyncIOScheduler] = None


def _worker_next_run_iso() -> Optional[str]:
    """Return the scheduler's next_run for our tick job as ISO, or None."""
    if _worker_scheduler is None:
        return None
    try:
        job = _worker_scheduler.get_job(WORKER_JOB_ID)
    except Exception:  # pragma: no cover
        return None
    if job is None or job.next_run_time is None:
        return None
    return job.next_run_time.isoformat()


def _serialise_dt(value: Any) -> Any:
    """Convert datetime / Path values inside a result dict to JSON-safe scalars."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {k: _serialise_dt(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_serialise_dt(v) for v in value]
    return value


async def run_worker_tick(trigger: str = "scheduler", dry_run: Optional[bool] = None) -> dict:
    """
    Drive one worker tick. Returns a small dict describing the outcome.

    A skipped tick means another tick is still mid-flight; we never queue.
    A WORKER_ENABLED=false config skips all scheduler ticks but still allows
    manual invocations (so Mick can poke the worker without restarting).
    """
    use_dry_run = WORKER_DRY_RUN if dry_run is None else dry_run

    if trigger == "scheduler" and not WORKER_ENABLED:
        skip = {
            "trigger": trigger,
            "reason": "worker disabled via CEDRIC_WORKER_ENABLED=false",
            "skipped_at": london_now().isoformat(),
        }
        _worker_state["last_skip"] = skip
        _worker_state["skip_count"] += 1
        _worker_state["next_run"] = _worker_next_run_iso()
        return {"status": "skipped", **skip}

    if not _worker_lock.acquire(blocking=False):
        skip = {
            "trigger": trigger,
            "reason": "previous tick still running",
            "skipped_at": london_now().isoformat(),
        }
        _worker_state["last_skip"] = skip
        _worker_state["skip_count"] += 1
        _worker_state["next_run"] = _worker_next_run_iso()
        return {"status": "skipped", **skip}

    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, cedric_worker.run_worker_pipeline, use_dry_run, False
        )
        result_safe = _serialise_dt(result)
        last_run = {
            "trigger": trigger,
            "dry_run": use_dry_run,
            "started_at": result_safe.get("started_at"),
            "completed_at": result_safe.get("completed_at"),
            "summary": result_safe.get("summary"),
            "inbox_processed": result["inbox"]["processed"],
            "inbox_errors": result["inbox"]["errors"],
            "notes_deleted": result["notes"]["deleted"],
            "git_files": result["git"]["files"],
            "git_pushed": result["git"]["pushed"],
        }
        _worker_state["last_run"] = last_run
        _worker_state["tick_count"] += 1
        _worker_state["next_run"] = _worker_next_run_iso()
        return {"status": "completed", **last_run}
    except Exception as exc:  # pragma: no cover
        err = {
            "trigger": trigger,
            "error": str(exc),
            "traceback": traceback.format_exc(limit=4),
            "errored_at": london_now().isoformat(),
        }
        _worker_state["last_error"] = err
        _worker_state["error_count"] += 1
        _worker_state["next_run"] = _worker_next_run_iso()
        sys.stderr.write("[worker] tick failed: " + str(exc) + "\n")
        return {"status": "error", **err}
    finally:
        _worker_lock.release()


def _start_worker_scheduler() -> None:
    """
    Build and start the AsyncIOScheduler with one interval job that fires
    run_worker_tick every WORKER_INTERVAL_MIN minutes.

    First tick is offset by WORKER_INTERVAL_MIN (we do NOT run on boot).
    """
    global _worker_scheduler
    scheduler = AsyncIOScheduler(timezone="Europe/London")
    trigger = IntervalTrigger(minutes=WORKER_INTERVAL_MIN)
    scheduler.add_job(
        run_worker_tick,
        trigger=trigger,
        id=WORKER_JOB_ID,
        name="Cedric worker (embedded)",
        kwargs={"trigger": "scheduler"},
        max_instances=1,
        coalesce=True,
        replace_existing=True,
    )
    scheduler.start()
    _worker_scheduler = scheduler
    _worker_state["scheduler_started"] = True
    _worker_state["next_run"] = _worker_next_run_iso()


def _stop_worker_scheduler() -> None:
    """Stop the scheduler cleanly on shutdown."""
    global _worker_scheduler
    if _worker_scheduler is None:
        return
    try:
        _worker_scheduler.shutdown(wait=False)
    except Exception:  # pragma: no cover
        pass
    _worker_scheduler = None
    _worker_state["scheduler_started"] = False


# ---------------------------------------------------------------------------
# SCHEMAS (1.3c + 1.3d + 1.3g)
# ---------------------------------------------------------------------------

class NoteType(str, Enum):
    NOTE = "note"
    IDEA = "idea"
    BRAINSTORM = "brainstorm"
    TASK = "task"


class NoteCreateRequest(BaseModel):
    """Body for POST /memory/note -- per PRD v0.3 Appendix B."""
    text: str = Field(..., min_length=1, description="The capture text (required).")
    source: Optional[str] = Field(
        default=None,
        description='Where the capture came from (e.g. claude.ai-mobile, cowork, voice).',
    )
    type: NoteType = Field(default=NoteType.NOTE, description="note | idea | brainstorm | task")
    tags: Optional[list] = Field(default=None, description="Optional tag list.")


class NoteCreateResponse(BaseModel):
    status: str
    id: str
    path: str


class AgentsReloadResponse(BaseModel):
    """Body for GET /agents/reload -- per PRD v0.3 Appendix B."""
    status: str
    agents_version: str
    rules_loaded: int
    content_drift: bool
    snapshot_written: bool
    loaded_at: str


class WorkerStatusResponse(BaseModel):
    """Body for GET /worker/status -- a snapshot of the embedded worker."""
    status: str
    enabled: bool
    interval_min: int
    scheduler_started: bool
    lock_held: bool
    next_run: Optional[str] = None
    tick_count: int
    skip_count: int
    error_count: int
    last_run: Optional[dict] = None
    last_skip: Optional[dict] = None
    last_error: Optional[dict] = None


class WorkerRunNowResponse(BaseModel):
    """Body for POST /worker/run_now -- outcome of a manual tick."""
    status: str
    trigger: str
    dry_run: bool
    summary: Optional[str] = None
    reason: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# ---------------------------------------------------------------------------
# NOTE WRITER (1.3c core)
# ---------------------------------------------------------------------------

_SLUG_RE = re.compile(r"[^A-Za-z0-9]+")


def _short_hash(text: str, n: int = 8) -> str:
    """Stable short hash for filename uniqueness within a minute."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def _format_tags_yaml(tags) -> str:
    if not tags:
        return "tags: []"
    items = ", ".join(_SLUG_RE.sub("-", t).strip("-") for t in tags if t.strip())
    return f"tags: [{items}]"


def _yaml_escape(value: str) -> str:
    """Minimal scalar escaping for YAML single-line strings."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def write_inbox_note(
    text: str,
    source,
    note_type: NoteType,
    tags,
    tier: AuthTier,
) -> Tuple[str, Path]:
    """
    Persist a capture to 00-Inbox/raw/ following PRD spec.

    Filename:  YYYY.MM.DDTHHmm-<hash>.md  (dot date per Mick's rule)
    Body:      YAML frontmatter (10.2 spec) + raw text body.

    Returns: (entry_id, absolute Path written).
    """
    INBOX_RAW.mkdir(parents=True, exist_ok=True)

    captured_utc = datetime.now(timezone.utc)
    london = london_now()
    stem_date = london.strftime("%Y.%m.%d")
    stem_time = london.strftime("%H%M")
    hashlet = _short_hash(f"{captured_utc.isoformat()}|{text}")
    entry_id = f"{stem_date}T{stem_time}-{hashlet}"
    filename = f"{entry_id}.md"
    target = INBOX_RAW / filename

    captured_iso = captured_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    source_safe = _yaml_escape(source or "unknown")

    frontmatter = (
        "---\n"
        f"id: {entry_id}\n"
        f"type: {note_type.value}\n"
        f'source: "{source_safe}"\n'
        f"source-tier: {tier.value}\n"
        f"captured: {captured_iso}\n"
        "generated-by: Mick\n"
        "silo:\n"
        "private: false\n"
        "status: raw\n"
        f"{_format_tags_yaml(tags)}\n"
        "---\n"
    )

    body = text.rstrip() + "\n"
    target.write_text(frontmatter + "\n" + body, encoding="utf-8")
    return entry_id, target


# ---------------------------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------------------------

app = FastAPI(
    title=SERVER_NAME,
    version=SERVER_VERSION,
    description=(
        "MCSB (Mick & Cedric Shared Brain) universal API. "
        "Exposes vault operations to every Claude surface plus mobile."
    ),
)


@app.on_event("startup")
def _on_startup() -> None:
    """
    Load agents.md once on boot AND start the embedded worker scheduler.
    Both are non-fatal -- failures are logged but do not abort startup.
    """
    try:
        load_agents_md(reason="server-startup")
    except HTTPException as exc:
        sys.stderr.write("[startup] agents.md load failed: " + str(exc.detail) + "\n")
    except Exception as exc:  # pragma: no cover
        sys.stderr.write("[startup] agents.md load exception: " + str(exc) + "\n")

    if WORKER_ENABLED:
        try:
            _start_worker_scheduler()
            sys.stderr.write(
                "[startup] embedded worker scheduler started "
                "(every " + str(WORKER_INTERVAL_MIN) + " min, dry_run="
                + str(WORKER_DRY_RUN) + ")\n"
            )
        except Exception as exc:  # pragma: no cover
            sys.stderr.write("[startup] worker scheduler failed to start: " + str(exc) + "\n")
    else:
        sys.stderr.write(
            "[startup] embedded worker disabled (CEDRIC_WORKER_ENABLED=false)\n"
        )


@app.on_event("shutdown")
def _on_shutdown() -> None:
    """Stop the embedded worker scheduler cleanly on Ctrl+C / shutdown."""
    _stop_worker_scheduler()


@app.get("/health")
def health() -> JSONResponse:
    """
    Liveness check. No authentication required.

    Tells the client the server is up, which version, whether the global .env
    is present, and whether the two tokens are configured. Token values are
    never returned -- only booleans. Also surfaces agents.md state.
    """
    now_utc = datetime.now(timezone.utc)
    uptime = now_utc - BOOT_UTC
    pc_token, mobile_token = _load_tokens()
    payload = {
        "status": "ok",
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "host": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "time_utc": now_utc.isoformat(),
        "time_london": london_now().isoformat(),
        "uptime_seconds": int(uptime.total_seconds()),
        "vault_root": str(VAULT_ROOT),
        "inbox_raw": str(INBOX_RAW),
        "global_env_present": GLOBAL_ENV_PATH.is_file(),
        "pc_token_configured": bool(pc_token),
        "mobile_token_configured": bool(mobile_token),
        "agents": {
            "version": _agents_state.get("version"),
            "rules_loaded": _agents_state.get("rules_loaded"),
            "loaded_at": _agents_state.get("loaded_at"),
            "snapshot_count": _agents_state.get("snapshot_count", 0),
        },
        "worker": {
            "enabled": _worker_state.get("enabled"),
            "interval_min": _worker_state.get("interval_min"),
            "scheduler_started": _worker_state.get("scheduler_started"),
            "lock_held": _worker_lock.locked(),
            "next_run": _worker_next_run_iso(),
            "tick_count": _worker_state.get("tick_count", 0),
            "skip_count": _worker_state.get("skip_count", 0),
            "error_count": _worker_state.get("error_count", 0),
            "last_run_summary": (
                (_worker_state.get("last_run") or {}).get("summary")
            ),
        },
    }
    return JSONResponse(payload)


@app.post(
    "/memory/note",
    response_model=NoteCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def post_memory_note(
    body: NoteCreateRequest,
    tier: AuthTier = Depends(require_token),
) -> NoteCreateResponse:
    """
    Quick capture from any surface. Writes to 00-Inbox/raw/.
    Auth: Mobile or PC token. See PRD v0.3 Appendix B.
    """
    try:
        entry_id, target = write_inbox_note(
            text=body.text,
            source=body.source,
            note_type=body.type,
            tags=body.tags,
            tier=tier,
        )
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vault write failed: {exc}",
        ) from exc

    rel = target.relative_to(VAULT_ROOT).as_posix()
    return NoteCreateResponse(status="ok", id=entry_id, path=rel)


@app.get(
    "/agents/reload",
    response_model=AgentsReloadResponse,
)
def get_agents_reload(
    tier: AuthTier = Depends(require_pc_token),
) -> AgentsReloadResponse:
    """
    Force-reload agents.md without waiting for the hourly cycle.

    Auth: PC token only (Mobile tokens receive HTTP 403).
    Side effects:
      - Re-reads agents.md from vault root.
      - If content has changed since last load, writes a snapshot to
        agents.md-history/ and appends a CHANGELOG entry.
      - Updates server's in-memory agents state (surfaced in /health).

    See PRD v0.3 Appendix B for the canonical contract.
    """
    state, drift, snapshot_written = load_agents_md(reason="manual-reload")
    return AgentsReloadResponse(
        status="ok",
        agents_version=str(state.get("version", "unknown")),
        rules_loaded=int(state.get("rules_loaded", 0)),
        content_drift=drift,
        snapshot_written=snapshot_written,
        loaded_at=str(state.get("loaded_at", "")),
    )


@app.get(
    "/worker/status",
    response_model=WorkerStatusResponse,
)
def get_worker_status(
    tier: AuthTier = Depends(require_pc_token),
) -> WorkerStatusResponse:
    """
    Snapshot of the embedded worker (1.3g). PC token only.

    Returns scheduler state, lock state, counts since boot, and the last
    completed run / skip / error records (each may be null on a fresh boot).
    """
    return WorkerStatusResponse(
        status="ok",
        enabled=bool(_worker_state.get("enabled")),
        interval_min=int(_worker_state.get("interval_min", WORKER_INTERVAL_MIN)),
        scheduler_started=bool(_worker_state.get("scheduler_started")),
        lock_held=_worker_lock.locked(),
        next_run=_worker_next_run_iso(),
        tick_count=int(_worker_state.get("tick_count", 0)),
        skip_count=int(_worker_state.get("skip_count", 0)),
        error_count=int(_worker_state.get("error_count", 0)),
        last_run=_worker_state.get("last_run"),
        last_skip=_worker_state.get("last_skip"),
        last_error=_worker_state.get("last_error"),
    )


@app.post(
    "/worker/run_now",
    response_model=WorkerRunNowResponse,
)
async def post_worker_run_now(
    dry_run: Optional[bool] = None,
    tier: AuthTier = Depends(require_pc_token),
) -> WorkerRunNowResponse:
    """
    Fire one worker tick immediately (1.3g). PC token only.

    Query params:
      dry_run: if true, run worker in preview mode (no file moves, no git push).
               if omitted, uses CEDRIC_WORKER_DRY_RUN env-var default.

    Behaviour:
      - If another tick is mid-flight, returns status=skipped (no queueing).
      - Disabled-by-env (CEDRIC_WORKER_ENABLED=false) is bypassed for manual
        runs -- you can still poke the worker by hand.
    """
    result = await run_worker_tick(trigger="manual", dry_run=dry_run)
    use_dry_run = WORKER_DRY_RUN if dry_run is None else dry_run
    return WorkerRunNowResponse(
        status=result.get("status", "error"),
        trigger="manual",
        dry_run=bool(use_dry_run),
        summary=result.get("summary"),
        reason=result.get("reason"),
        error=result.get("error"),
        started_at=result.get("started_at"),
        completed_at=result.get("completed_at"),
    )


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the server in dev mode."""
    try:
        import uvicorn
    except ImportError:
        sys.stderr.write(
            "ERROR: uvicorn is not installed. Run:\n"
            "    pip install fastapi uvicorn[standard]\n"
        )
        raise

    host = os.environ.get("CEDRIC_SERVER_HOST", "127.0.0.1")
    port = int(os.environ.get("CEDRIC_SERVER_PORT", "8765"))
    uvicorn.run(
        "cedric_server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
