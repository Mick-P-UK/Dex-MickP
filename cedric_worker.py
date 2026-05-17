#!/usr/bin/env python3
"""
cedric_worker.py -- MCSB Phase 1.2
Cedric Server hourly worker.

Duties (in order):
  1. Process 00-Inbox/raw/ items  (classify, wiki-link, move to processed/)
  2. Delete confirmed-blank daily notes before commit
  3. Git commit + push vault to GitHub
  4. Write structured audit lines to log.md

Run via Windows Task Scheduler (hourly) for Phase 1.
In Phase 1.3 this module is imported and called by the Cedric Server
as a background task -- no changes needed, just import and schedule.

Usage:
  python cedric_worker.py           # run once
  python cedric_worker.py --dry-run # preview only, no changes

MCSB Decision D25: CHANGELOG.md at server root tracks deployments.
MCSB Decision D26: 08-People/ and 09-Entities/ (renumbered from 02/03).
"""

import os
import re
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

VAULT = Path(r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP")

INBOX_RAW      = VAULT / "00-Inbox" / "raw"
INBOX_DONE     = VAULT / "00-Inbox" / "raw" / "processed"
LOG_FILE       = VAULT / "log.md"
AGENTS_FILE    = VAULT / "agents.md"

ENTITY_PATHS   = [
    VAULT / "09-Entities" / "Tickers",
    VAULT / "09-Entities" / "Companies",
    VAULT / "09-Entities" / "Concepts",
    VAULT / "08-People",
]

# Daily notes live in the vault root or a dated subfolder.
# Obsidian Core Daily Notes default: YYYY-MM-DD.md at vault root.
DAILY_NOTE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

# A daily note is "blank" if it has no meaningful content beyond these.
BLANK_NOTE_MARKERS = {
    "",                          # completely empty
}
BLANK_NOTE_MAX_LINES = 5        # <= this many lines AND no substantive content = blank

# Classification keyword map (rule-based, Phase 1)
# Phase 2 will replace this with LLM classification.
CLASSIFY_KEYWORDS = {
    "meeting":   ["meeting", "call", "catch-up", "catchup", "zoom", "teams", "agenda"],
    "idea":      ["idea", "brainstorm", "concept", "thought", "what if", "could we"],
    "task":      ["todo", "to-do", "action", "task", "follow up", "follow-up", "remind"],
    "reference": ["reference", "resource", "link", "article", "source", "note from"],
}
# Default classification if no keywords match
DEFAULT_TYPE = "note"


# ---------------------------------------------------------------------------
# LOGGING TO log.md
# ---------------------------------------------------------------------------

def london_now() -> str:
    """Return current London time as ISO string (BST or GMT)."""
    utc = datetime.now(timezone.utc)
    bst = 4 <= utc.month <= 10
    local = utc.astimezone(timezone(timedelta(hours=1 if bst else 0)))
    return local.strftime("%Y-%m-%d %H:%M:%S")


def append_log(action: str, file: str, result: str, dry_run: bool = False):
    """Append a single structured audit line to log.md."""
    line = f"{london_now()} | {action:<22} | {file:<50} | {result}\n"
    if dry_run:
        print(f"  [DRY-RUN] LOG: {line.strip()}")
        return
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"  [WARNING] Could not write to log.md: {e}")


# ---------------------------------------------------------------------------
# STEP 1: INBOX PROCESSING
# ---------------------------------------------------------------------------

def load_entity_names() -> list[str]:
    """
    Return a sorted list of entity/person names from vault folders.
    Used for wiki-link injection.
    Names derived from filenames (stem only, no extension).
    Sorted longest-first so longer names match before substrings.
    """
    names = []
    for folder in ENTITY_PATHS:
        if folder.exists():
            for f in folder.iterdir():
                if f.suffix == ".md" and f.stem not in (".gitkeep",):
                    names.append(f.stem)
    names.sort(key=len, reverse=True)
    return names


def classify_item(content: str, filename: str) -> str:
    """
    Rule-based classification (Phase 1).
    Check frontmatter 'type:' first, then filename, then content keywords.
    Returns one of: note / idea / meeting / reference / task
    """
    # 1. Frontmatter type field
    fm_match = re.search(r"^type:\s*(\S+)", content, re.MULTILINE | re.IGNORECASE)
    if fm_match:
        fm_type = fm_match.group(1).strip().lower().strip("'\"")
        if fm_type in CLASSIFY_KEYWORDS or fm_type == "note":
            return fm_type

    # 2. Filename keywords
    fname_lower = filename.lower()
    for type_name, keywords in CLASSIFY_KEYWORDS.items():
        if any(kw in fname_lower for kw in keywords):
            return type_name

    # 3. Content keywords
    content_lower = content.lower()
    for type_name, keywords in CLASSIFY_KEYWORDS.items():
        if any(kw in content_lower for kw in keywords):
            return type_name

    return DEFAULT_TYPE


def inject_wiki_links(content: str, entity_names: list[str]) -> tuple[str, int]:
    """
    Replace plain entity name mentions with [[wiki links]].
    Skips names already inside [[ ]].
    Returns (modified_content, count_of_links_added).
    """
    count = 0
    for name in entity_names:
        # Match name as whole word, not already inside [[ ]]
        pattern = r"(?<!\[\[)\b(" + re.escape(name) + r")\b(?!\]\])"
        new_content, n = re.subn(pattern, r"[[\1]]", content, flags=re.IGNORECASE)
        if n > 0:
            content = new_content
            count += n
    return content, count


def add_frontmatter_field(content: str, field: str, value: str) -> str:
    """
    Add or update a field inside existing YAML frontmatter.
    If no frontmatter, wraps the content.
    """
    if content.startswith("---"):
        # Find closing ---
        end = content.find("\n---", 3)
        if end != -1:
            fm = content[:end]
            rest = content[end:]
            # Update or insert field
            field_pat = re.compile(rf"^{re.escape(field)}:.*$", re.MULTILINE)
            if field_pat.search(fm):
                fm = field_pat.sub(f"{field}: {value}", fm)
            else:
                fm = fm.rstrip() + f"\n{field}: {value}"
            return fm + rest
    # No frontmatter -- prepend
    return f"---\n{field}: {value}\n---\n\n" + content


def process_inbox(dry_run: bool = False) -> dict:
    """
    Process all .md files in 00-Inbox/raw/ (excluding processed/ subfolder).
    Returns summary dict.
    """
    results = {"processed": 0, "skipped": 0, "errors": 0}

    if not INBOX_RAW.exists():
        print("  [WARN] 00-Inbox/raw/ does not exist -- skipping inbox processing")
        return results

    entity_names = load_entity_names()
    print(f"  Loaded {len(entity_names)} entity names for wiki-linking")

    files = [
        f for f in INBOX_RAW.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name != "README.md"
    ]

    if not files:
        print("  No files to process in 00-Inbox/raw/")
        return results

    print(f"  Found {len(files)} file(s) to process")

    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
            original_content = content

            # Classify
            item_type = classify_item(content, filepath.name)

            # Add/update frontmatter fields
            content = add_frontmatter_field(content, "cedric-type", item_type)
            content = add_frontmatter_field(content, "cedric-processed", london_now())

            # Wiki-link injection
            content, links_added = inject_wiki_links(content, entity_names)

            # Destination
            dest = INBOX_DONE / filepath.name
            # Avoid overwriting -- suffix with timestamp if needed
            if dest.exists():
                stem = filepath.stem
                suffix = filepath.suffix
                ts = datetime.now().strftime("%H%M%S")
                dest = INBOX_DONE / f"{stem}-{ts}{suffix}"

            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content, encoding="utf-8")
                filepath.unlink()  # remove from raw/ after moving to processed/

            print(f"    -> {filepath.name} | type={item_type} | links={links_added}")
            append_log("INBOX_PROCESSED", filepath.name,
                       f"type={item_type} links={links_added} -> {dest.name}", dry_run)
            results["processed"] += 1

        except Exception as e:
            print(f"    [ERROR] {filepath.name}: {e}")
            append_log("INBOX_ERROR", filepath.name, str(e), dry_run)
            results["errors"] += 1

    return results


# ---------------------------------------------------------------------------
# STEP 2: BLANK DAILY NOTE CLEANUP
# ---------------------------------------------------------------------------

def is_blank_daily_note(filepath: Path) -> bool:
    """
    Return True if a daily note contains no meaningful content.
    Criteria: <= BLANK_NOTE_MAX_LINES lines, all are empty/whitespace/yaml markers/headings only.
    """
    try:
        content = filepath.read_text(encoding="utf-8").strip()
        if not content:
            return True

        lines = [l.strip() for l in content.splitlines()]

        # Strip YAML frontmatter block if present
        if lines and lines[0] == "---":
            try:
                end_fm = lines.index("---", 1)
                lines = lines[end_fm + 1:]
            except ValueError:
                pass

        # Remove empty lines
        meaningful = [l for l in lines if l and not l.startswith("#")]
        return len(meaningful) == 0

    except Exception:
        return False


def cleanup_blank_daily_notes(dry_run: bool = False) -> dict:
    """
    Find and delete confirmed-blank daily notes from vault root.
    Returns summary dict.
    """
    results = {"deleted": 0, "checked": 0}

    if not VAULT.exists():
        print(f"  [WARN] Vault path not found: {VAULT} -- skipping daily note cleanup")
        return results

    daily_notes = [
        f for f in VAULT.iterdir()
        if f.is_file() and DAILY_NOTE_PATTERN.match(f.name)
    ]

    results["checked"] = len(daily_notes)

    for note in daily_notes:
        if is_blank_daily_note(note):
            print(f"  Deleting blank daily note: {note.name}")
            if not dry_run:
                note.unlink()
            append_log("DAILY_NOTE_DELETED", note.name, "blank note removed", dry_run)
            results["deleted"] += 1

    if results["deleted"] == 0:
        print(f"  No blank daily notes found (checked {results['checked']})")

    return results


# ---------------------------------------------------------------------------
# STEP 3: GIT COMMIT + PUSH
# ---------------------------------------------------------------------------

def git_run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=str(VAULT)
    )


def git_commit_and_push(dry_run: bool = False) -> dict:
    """
    Stage all changes, commit with structured message, push to GitHub.
    Returns summary dict.
    """
    results = {"committed": False, "pushed": False, "files": 0, "message": ""}

    # Check for changes
    status = git_run("git status --porcelain")
    if not status.stdout.strip():
        print("  No changes to commit")
        append_log("GIT_COMMIT", "vault", "no changes", dry_run)
        return results

    changed_lines = [l for l in status.stdout.strip().splitlines() if l.strip()]
    results["files"] = len(changed_lines)

    ts = london_now()
    msg = f"Cedric worker {ts} | {results['files']} file(s) changed"

    print(f"  {results['files']} changed file(s) -- committing")
    results["message"] = msg

    if dry_run:
        print(f"  [DRY-RUN] Would commit: {msg}")
        return results

    # Stage
    stage = git_run("git add .")
    if stage.returncode != 0:
        print(f"  [ERROR] git add failed: {stage.stderr.strip()}")
        append_log("GIT_ERROR", "git add", stage.stderr.strip()[:80], dry_run)
        return results

    # Commit
    commit = git_run(f'git commit -m "{msg}"')
    if commit.returncode == 0:
        results["committed"] = True
        print(f"  Committed: {msg}")
        append_log("GIT_COMMIT", "vault", f"files={results['files']}", dry_run)
    else:
        err = commit.stderr.strip() or commit.stdout.strip()
        if "nothing to commit" in err:
            print("  Nothing to commit (all changes ignored)")
        else:
            print(f"  [ERROR] git commit failed: {err}")
            append_log("GIT_ERROR", "git commit", err[:80], dry_run)
        return results

    # Push
    push = git_run("git push")
    if push.returncode == 0:
        results["pushed"] = True
        print("  Pushed to GitHub")
        append_log("GIT_PUSH", "origin", "success", dry_run)
    else:
        err = push.stderr.strip()
        print(f"  [ERROR] git push failed: {err}")
        append_log("GIT_ERROR", "git push", err[:80], dry_run)

    return results


# ---------------------------------------------------------------------------
# PIPELINE ENTRY POINT (CLI-independent -- imported by cedric_server.py)
# ---------------------------------------------------------------------------

def run_worker_pipeline(dry_run: bool = False, verbose: bool = False) -> dict:
    """
    Run the full worker pipeline (inbox -> blank-note cleanup -> git push)
    and return a structured summary.

    CLI-independent; safe to import and call. This is the entry point
    cedric_server.py uses for embedded background ticks (MCSB Phase 1.3g).

    Args:
        dry_run: Preview only -- no files moved, no git changes.
        verbose: Print step-by-step progress to stdout (CLI mode).

    Returns:
        dict with started_at, completed_at, dry_run, inbox, notes, git, summary.
    """
    start_ts = london_now()
    if verbose:
        marker = "[DRY-RUN]" if dry_run else ""
        print("=== Cedric Worker started: " + str(start_ts) + " " + marker + " ===")
        print()
    append_log("WORKER_START", "cedric_worker.py", "dry_run=" + str(dry_run), dry_run)

    # Step 1: Inbox
    if verbose:
        print("Step 1: Processing inbox...")
    inbox_results = process_inbox(dry_run)
    if verbose:
        print("  Done: " + str(inbox_results["processed"]) + " processed, "
              + str(inbox_results["errors"]) + " errors")
        print()

    # Step 2: Blank daily notes
    if verbose:
        print("Step 2: Cleaning blank daily notes...")
    notes_results = cleanup_blank_daily_notes(dry_run)
    if verbose:
        print("  Done: " + str(notes_results["deleted"]) + " deleted of "
              + str(notes_results["checked"]) + " checked")
        print()

    # Step 3: Git commit + push
    if verbose:
        print("Step 3: Git commit and push...")
    git_results = git_commit_and_push(dry_run)
    if verbose:
        print()

    end_ts = london_now()
    summary = ("inbox=" + str(inbox_results["processed"]) +
               " notes_deleted=" + str(notes_results["deleted"]) +
               " git_files=" + str(git_results["files"]) +
               " pushed=" + str(git_results["pushed"]))
    if verbose:
        print("=== Cedric Worker complete: " + str(end_ts) + " | " + summary + " ===")
    append_log("WORKER_DONE", "cedric_worker.py", summary, dry_run)

    return {
        "started_at": start_ts,
        "completed_at": end_ts,
        "dry_run": dry_run,
        "inbox": inbox_results,
        "notes": notes_results,
        "git": git_results,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# MAIN (CLI wrapper)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Cedric hourly worker -- MCSB Phase 1")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview only -- no files moved, no git changes, no log writes")
    args = parser.parse_args()
    run_worker_pipeline(dry_run=args.dry_run, verbose=True)


if __name__ == "__main__":
    main()
