# Cedric Server -- CHANGELOG

All notable changes to the Cedric Server code are logged here.
Format: one entry per deployment (PRD v0.3 D25).

Versioning: SemVer (MAJOR.MINOR.PATCH).
Dates are ISO-8601 (YYYY-MM-DD), London local.

---

## [0.4.0] -- 2026-05-17

cedric_worker.py embedded as a FastAPI background scheduler task (1.3g),
finishing the Cedric Server v0.1 series. Windows Task Scheduler dependency
now removable.

### Added
- APScheduler (AsyncIOScheduler) embedded in the FastAPI app. One job,
  IntervalTrigger every `CEDRIC_WORKER_INTERVAL_MIN` minutes (default 60),
  London timezone. Job id: `cedric_worker_tick`.
- `GET /worker/status` -- snapshot of the embedded worker. PC token only.
  Returns: `{ status, enabled, interval_min, scheduler_started, lock_held,
  next_run, tick_count, skip_count, error_count, last_run, last_skip,
  last_error }`. last_run/skip/error are null on a fresh boot.
- `POST /worker/run_now` -- fire one tick immediately. PC token only.
  Optional query param `dry_run` overrides the env-var default for the call.
- `threading.Lock` non-blocking acquire around each tick. If a tick is
  already mid-flight, the new call is recorded as `status=skipped` with
  reason `"previous tick still running"` rather than queued. Prevents
  pile-up if a git push stalls.
- Clean shutdown hook (`@app.on_event("shutdown")`) stops the scheduler so
  Ctrl+C exits cleanly. No orphaned threads.
- `/health` payload now includes a `worker` block: `{ enabled, interval_min,
  scheduler_started, lock_held, next_run, tick_count, skip_count,
  error_count, last_run_summary }`.
- Tiny shim in cedric_worker.py: new `run_worker_pipeline(dry_run, verbose)`
  function provides a CLI-independent entry point. Existing `main()` is
  now a 4-line CLI wrapper around it. Behaviour unchanged for the
  standalone Task Scheduler path.

### Env vars new in v0.4.0
- `CEDRIC_WORKER_ENABLED` -- default "true". Set "false" to disable the
  scheduled tick path. Manual `/worker/run_now` still works when disabled
  (so Mick can poke the worker by hand for debugging).
- `CEDRIC_WORKER_INTERVAL_MIN` -- default "60". Minutes between scheduled
  ticks. Floor of 1.
- `CEDRIC_WORKER_DRY_RUN` -- default "false". When "true", all ticks
  (scheduled and manual without explicit override) run in preview mode:
  no file moves, no git changes, no log writes. Useful for sandbox/staging.

### Design notes
- APScheduler chosen over hand-rolled asyncio loop. Tiny dep, well-trodden,
  scales cleanly when Phase 5 adds `/briefing/today` and Phase 6 adds
  theme-mining / contradiction-detection jobs (DEC-S5-01).
- threading.Lock used (not asyncio.Lock) because the critical section runs
  inside `run_in_executor` on a worker thread; the lock guards against
  re-entrant invocations from both the scheduler and `/worker/run_now`.
- First tick is offset by `WORKER_INTERVAL_MIN` (no boot tick). Matches
  the prior Windows Task Scheduler behaviour and keeps the startup hook
  cheap (DEC-S5-02).
- ASCII-only outputs preserved throughout. Worker shim preserves the same
  output format as before for the standalone CLI path.

### Tested
- 25/25 paths green in the Linux sandbox before deployment:
  module load + startup hook, /health worker block contents, /worker/status
  auth matrix (no-auth/mobile/PC), tick_count + lock_held semantics,
  /worker/run_now auth matrix, successful tick + tick_count increment +
  last_run.summary populated, lock-contention -> skipped, regression on
  POST /memory/note (mobile) and GET /agents/reload (PC + mobile).

### Build context
- Phase: MCSB Phase 1.3 (Cedric Server v0.1 series) -- COMPLETE with
  this release.
- Sub-steps completed THIS release: 1.3g (embedded worker as background task).
- Sub-steps remaining in Phase 1: none in the 1.3 series. Phase 1 moves on
  to 1.4 (agents.md framework finalisation, mostly already done) and 1.5
  (MCP wrapper v0.1).
- Deferred (not blocking 1.3 closure): Windows service install; token
  rotation before Cloudflare tunnel work; Task Scheduler job deletion
  (planned for Session 6 after one observation cycle).

---

## [0.3.0] -- 2026-05-17

`/agents/reload` endpoint plus the PC-only auth tier (1.3e completion).

### Added
- `GET /agents/reload` -- forces an agents.md reload without waiting for the
  hourly worker cycle. Per PRD v0.3 Appendix B.
  Auth: PC token only (Mobile tokens get HTTP 403).
  Response shape: `{ status, agents_version, rules_loaded, content_drift,
  snapshot_written, loaded_at }`.
- `require_pc_token` FastAPI dependency -- the 1.3e 403 tier guard. Mobile
  tokens are rejected with HTTP 403 + `"PC token required for this endpoint."`
  This pattern will be reused by `/memory/search_all` and `/briefing/today`
  in later phases.
- agents.md loader (`load_agents_md`) -- parses YAML frontmatter for the
  `version` field, counts top-level rule blocks, hashes content, and updates
  module state. Called once on server startup (FastAPI `on_event("startup")`)
  and again on every `/agents/reload`.
- Automatic history snapshots on content change -- snapshots are written to
  `agents.md-history/agents-v<VERSION>-<YYYY.MM.DDTHHMMSS>-<hash6>.md`.
  Filename includes seconds and a 6-char content hash so two reloads in the
  same minute never collide on disk.
- Auto-append to `agents.md-history/CHANGELOG.md` on every snapshot, newest
  first, including the reason (`server-startup` or `manual-reload`) and the
  Cedric Server version that wrote it.
- Drift detection -- when content changes but the `version:` frontmatter
  field does NOT, the reload response sets `content_drift: true` and the
  CHANGELOG entry is tagged `(content drift -- version not bumped)`.
- `/health` payload now includes an `agents` block with `version`,
  `rules_loaded`, `loaded_at`, and `snapshot_count`.

### Design notes
- Versioning model is "Option 1 + extension" (decided this session):
  the `version:` field in agents.md frontmatter is the source of truth for
  what's loaded; the server NEVER mutates it. Content-hash drift is reported
  as a separate boolean in the reload response, not bolted onto the version
  string. Keeps the version field clean for downstream consumers (MCP wrapper,
  /health, etc.).
- The startup hook silently no-ops on a missing or malformed agents.md so
  the server still boots and `/health` still answers. `/agents/reload`,
  however, returns HTTP 500 with a clear `agents.md not found at <path>`
  detail so Mick knows what to fix.
- ASCII-only outputs preserved throughout.

### Tested
- 18/18 paths green in the Linux sandbox before deployment:
  startup hook, full auth matrix (no/bogus/mobile/PC), idempotent reload,
  version-bump snapshot, drift-detection snapshot, 6-snapshot rapid-fire
  uniqueness, `/memory/note` regression (PC + mobile), `/health` integration,
  and missing-file edge case. See PROGRESS.md session 4 for the full log.

### Build context
- Phase: MCSB Phase 1.3 (Cedric Server v0.1 series)
- Sub-steps completed THIS release: 1.3d (`/agents/reload`) + 1.3e
  (PC-only 403 guard now in place, completing the auth scaffold).
- Sub-steps remaining: 1.3g (embed `cedric_worker.py` as background task).
  Plus: Windows service install (deferred, not blocking).

---

## [0.2.0] -- 2026-05-15

First write endpoint plus the two-tier bearer auth scaffold.

### Added
- `POST /memory/note` -- quick capture endpoint, per PRD v0.3 Appendix B.
  Accepts `text` (required), `source`, `type` (note|idea|brainstorm|task,
  default note) and `tags`. Writes a YAML-frontmatter Markdown file to
  `00-Inbox/raw/YYYY.MM.DDTHHmm-<hash>.md`. Returns
  `{ status, id, path }` with `path` relative to the vault root.
- Two-tier bearer-token auth scaffold (PRD v0.3 Appendix B, D4):
  - `MCSB_PC_TOKEN` -- full access (reserved for `/search_all` + private content).
  - `MCSB_MOBILE_TOKEN` -- restricted access.
  Both loaded on every request from `C:\Users\pavey\.env` so tokens can be
  rotated without a server restart. Bearer header is `Authorization: Bearer <token>`.
  Missing or invalid token returns HTTP 401 with `WWW-Authenticate: Bearer`.
- `generate_tokens.py` helper -- prints two random 32-byte hex tokens for
  Mick to paste into `.env`. Does NOT touch the .env file itself.
- `/health` now also reports `pc_token_configured` and `mobile_token_configured`
  (booleans only; token values are never returned by any endpoint).
- `/health` now reports `inbox_raw` for verification of the capture target.

### Notes
- The hourly vault worker (`cedric_worker.py`) is STILL not yet embedded;
  it continues to run via Windows Task Scheduler. Worker integration is
  scheduled for a later 1.3g step.
- ASCII-only outputs preserved -- no em dashes, smart quotes, or ellipsis
  in generated files (per vault rule).

### Build context
- Phase: MCSB Phase 1.3 (Cedric Server v0.1 series)
- Sub-steps completed: 1.3c (/memory/note) + 1.3e scaffold (bearer auth).
- Sub-steps remaining: 1.3d (/agents/reload), 1.3g (worker embed).
- Live-tested in sandbox before deployment -- see PROGRESS.md session 3.

---

## [0.1.0] -- 2026-05-15

Initial Cedric Server skeleton.

### Added
- FastAPI app skeleton (`cedric_server.py`).
- `GET /health` endpoint -- liveness check, no auth required. Returns server
  name, version, host, platform, Python version, UTC and London timestamps,
  uptime in seconds, vault root path, and presence flag for the global .env
  file at C:\Users\pavey\.env.
- Launcher script `run_cedric_server.bat` for local development runs.
- This CHANGELOG.md at the server root (PRD v0.3 D25).

### Notes
- Auth is not implemented in 0.1.0 -- `/health` is intentionally public so
  uptime monitors (and the Cloudflare tunnel) can probe without credentials.
- The hourly vault worker (`cedric_worker.py`) is NOT yet embedded; it still
  runs via Windows Task Scheduler. Embedding is scheduled for v0.2.0.
- Windows service registration is deferred to a follow-up session.

### Build context
- Phase: MCSB Phase 1.3 (Cedric Server v0.1)
- Sub-steps completed: 1.3a (FastAPI skeleton) + 1.3b (/health endpoint)
- Sub-steps remaining: 1.3c (/memory/note), 1.3d (/agents/reload),
  1.3e (bearer auth), 1.3g (worker integration). Windows service install: TBC.
