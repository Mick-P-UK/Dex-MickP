# Install: paypal-to-xero skill

Staged in this workspace because Cedric cannot write directly to the
skills vault from the DB-Accounts-CW project. Mick: please copy the
skill folder into the skills vault using PowerShell.

## What is in this folder

- `SKILL.md` - the skill definition (frontmatter + procedure)
- `scripts/convert.py` - the conversion script (run by the skill or
  directly from CLI)
- `INSTALL.md` - this file

## Installation (PowerShell, Windows)

```powershell
# Copy the skill folder into your skills vault
Copy-Item -Path "C:\Vaults\DB-Accounts-CW\YE_2025.11.30\workings\paypal-to-xero" `
          -Destination "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\" `
          -Recurse `
          -Force

# Verify it landed
Get-ChildItem "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\paypal-to-xero"
```

The vault folder mirrors to `/mnt/skills/user/` inside Cedric's
sandbox, so the skill becomes available next time you start a new
Cowork session in any project that has the skills mount enabled.

## Verification once installed

Next time you start a Cowork session, ask Cedric to "list skills" or
"run the paypal-to-xero skill" - it should show up in the skill list
alongside cc1136-to-xero, natwest-to-xero, ii-to-xero, and the others.

## Test run after installation

Easiest test: run the script directly against the YE 2025.11.30 source
that has already been imported and proven good. The output should be
byte-identical to the file you imported.

```powershell
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\paypal-to-xero"
python scripts\convert.py `
  --input "C:\path\to\PayPal-export.CSV" `
  --output-dir "C:\Vaults\DB-Accounts-CW\YE_2025.11.30\workings\test-skill-output" `
  --account-code 058 `
  --account-prefix "D.Box_PayPal" `
  --ye-year 2025 `
  --date-today 2026.05.29
```

The script prints a per-step report and exits 0 if the three-way
reconciliation ties. The output CSV should match
`2026.05.29 - D.Box_PayPal-058_Xero-import_YE_2025_DRAFT.csv`
byte-for-byte.

## Validation history

Confirmed by Cedric in Session 08 (2026.05.29):
- YE 2025.11.30 skill output is byte-identical to the file Mick
  imported successfully into Xero account 058 (closing +234.38).
- YE 2024.11.30 skill output matches Mick's manual v.07 from May 2025
  on date+amount for all 25 rows. Contextual annotations
  ("(Plaza Subscription)", "(Wordfence)" etc.) and the carry-forward
  payee on User Initiated Withdrawal are the only deltas - by design,
  these are flagged in the Review Annotation column of the audit XLSX
  for manual fill.
