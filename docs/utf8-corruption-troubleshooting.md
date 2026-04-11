# UTF-8 Corruption: Troubleshooting & Prevention

**Last Updated:** 2026-02-22
**Status:** Resolved - pre-commit hook active

---

## The Problem

Certain typographic characters that Windows and word processors insert automatically
(em dashes, smart/curly quotes, ellipsis, non-breaking spaces, etc.) are encoded in
Windows-1252, not UTF-8. They look perfectly fine in Obsidian and text editors, but
the work-mcp Python tools use strict UTF-8 file reading and crash with:

```
'utf-8' codec can't decode byte 0x97 in position 301: invalid start byte
```

This blocks ALL work-mcp tools (get_system_status, list_tasks, create_task, etc.)
until the offending character is removed.

---

## Characters That Cause This

| Byte  | Character         | Looks Like      | Safe Replacement |
|-------|-------------------|-----------------|------------------|
| 0x80  | Euro sign         | EUR symbol      | EUR              |
| 0x85  | Ellipsis          | ...             | ...              |
| 0x91  | Left single quote | '               | '                |
| 0x92  | Right single quote| '               | '                |
| 0x93  | Left double quote | "               | "                |
| 0x94  | Right double quote| "               | "                |
| 0x95  | Bullet            | *               | -                |
| 0x96  | En dash           | --              | -                |
| 0x97  | Em dash           | ---             | -                |
| 0x99  | Trade mark        | (TM)            | (TM)             |
| 0xA0  | Non-breaking space| (invisible)     | (space)          |

Common sources: copy-paste from Word/web, voice dictation, Obsidian autocorrect
(if Smart Punctuation is enabled).

---

## How to Fix It (Step-by-Step)

### Step 1: Identify the file and location

The error message gives you the byte position but not the file. Run this to find it:

```powershell
# From the vault root (Dex-MickP folder)
python -c "
import os, glob
BANNED = set(range(0x80, 0xa1))
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'rb') as fh:
                data = fh.read()
            hits = [(i, b) for i, b in enumerate(data) if b in BANNED]
            if hits:
                for pos, b in hits:
                    line = data[:pos].count(b'\n') + 1
                    print(f'{path}  line {line}  pos {pos}  byte 0x{b:02X}')
"
```

### Step 2: Fix the character

Open the file in Obsidian or any text editor, go to the line shown, and replace
the character with its plain ASCII equivalent (see table above).

Or fix it programmatically (safer for binary-level issues):

```powershell
python -c "
path = r'03-Tasks\2026.02.07-Tasks.md'  # adjust path as needed
with open(path, 'rb') as f:
    data = f.read()

replacements = {
    b'\x97': b'-',   # em dash
    b'\x96': b'-',   # en dash
    b'\x91': b\"'\", # left single quote
    b'\x92': b\"'\", # right single quote
    b'\x93': b'\"',  # left double quote
    b'\x94': b'\"',  # right double quote
    b'\x85': b'...',  # ellipsis
    b'\x95': b'-',   # bullet
    b'\xa0': b' ',   # non-breaking space
}
for old, new in replacements.items():
    data = data.replace(old, new)

with open(path, 'wb') as f:
    f.write(data)
print('Fixed.')
"
```

### Step 3: Verify and re-stage

```powershell
# Verify the file is now clean
python -c "
with open(r'03-Tasks\2026.02.07-Tasks.md', 'rb') as f:
    data = f.read()
data.decode('utf-8')
print('Clean.')
"

# Re-stage and commit
git add .
git commit -m "fix: remove typographic characters from Tasks.md"
```

---

## Prevention: Pre-Commit Hook

A git pre-commit hook is installed at `.git/hooks/pre-commit`. It automatically
scans all staged `.md` files before every commit and blocks any that contain
the banned characters, showing exactly where the problem is.

**The hook runs automatically** - you don't need to do anything. If a commit is
blocked, it will show output like:

```
============================================================
  COMMIT BLOCKED: Typographic characters detected
  These break work-mcp's UTF-8 file reader.
============================================================

  File: 03-Tasks/Tasks.md
    Line 18, pos 301: 0x97 (Em dash)
    Replace with: '-'
    Context: ...Schedule around 4th Mar -- find a free...

  Fix the above, then re-stage (git add) and commit again.
  Quick find: grep -P '[\x80-\x9F\xA0]' <filename>
============================================================
```

### If the hook stops running

This can happen if git loses track of the hooks path. Fix with:

```powershell
# From the vault root (Dex-MickP folder)
git config core.hooksPath .git/hooks
```

Then verify the hook file exists:
```powershell
ls .git\hooks\pre-commit
```

If missing, ask Cedric to recreate it - the source is documented in CUSTOM_CHANGES.md
(2026-02-22 entry).

### If you need to bypass the hook (emergency only)

```powershell
git commit --no-verify -m "your message"
```

**Warning:** Only use this if you have a genuine reason to commit a file with
known issues. Fix the corruption as soon as possible afterwards.

---

## Prevention: Obsidian Setting

In Obsidian: **Settings > Editor > Smart Punctuation > OFF**

This stops Obsidian auto-converting:
- `--` to em dash
- `"text"` to smart/curly quotes

---

## History

| Date       | What happened                                          |
|------------|--------------------------------------------------------|
| 2026-02-22 | Em dash (0x97) in `2026.02.07-Tasks.md` at pos 301 blocked all work-mcp tools. Fixed manually. Pre-commit hook installed to prevent recurrence. |

---

*If you hit this again and the above doesn't help, ask Cedric. The fix is always
the same: find the byte, replace it, re-commit.*
