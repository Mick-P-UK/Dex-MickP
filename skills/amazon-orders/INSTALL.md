# Install: amazon-orders skill

Staged in this workspace because Cedric cannot write to the skills vault or the
plugin folder from the DB-Accounts-CW project (both are outside the connected
folder). Mick installs it with a single PowerShell dual-write, then a new Cedric
session picks it up.

## What is in this folder

- `SKILL.md`  - the skill definition (frontmatter + full procedure)
- `scripts/build_schedule.py` - combines the chunk CSVs, dedupes, filters the FY
  window, reconciles vs the master, and builds the landscape per-item XLSX
- `INSTALL.md` - this file

## Install (PowerShell, Windows) - DUAL WRITE

The vault is the source of truth; the plugin folder is where Cedric actually
loads skills at session start. Both must be updated. Single pasteable line:

```powershell
$src='C:\Vaults\DB-Accounts-CW\YE_2025.11.30\workings\amazon-orders'; $vault="C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\amazon-orders"; $plugin='C:\Users\pavey\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\d8019982-7ac8-4e6f-8866-902876b7d6e8\725a0328-db69-40d6-8d55-440c58b55304\skills\amazon-orders'; foreach($d in @($vault,$plugin)){ if(Test-Path $d){Remove-Item $d -Recurse -Force}; Copy-Item $src $d -Recurse -Force; Write-Host "installed -> $d" }
```

## Verify installed

```powershell
Get-ChildItem "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\amazon-orders" -Recurse | Select-Object FullName
```

Then start a NEW Cowork session and ask Cedric to "list skills" - amazon-orders
should appear alongside cc1136-to-xero, natwest-to-xero, ii-to-xero,
schwab-to-xero and paypal-to-xero. (The install is async: it does not show up in
the session where it was staged.)

## Test run after install

Fastest test - run the script against this year's chunks, which are already
proven good, and confirm it reproduces the schedule:

```powershell
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\amazon-orders"
python scripts\build_schedule.py `
  --chunks-dir "C:\Vaults\DB-Accounts-CW\YE_2025.11.30\workings" `
  --fy-year 2025 `
  --output-dir "C:\Vaults\DB-Accounts-CW\YE_2025.11.30\workings\test-skill-output" `
  --date-today 2026.07.13 `
  --master "C:\Vaults\DB-Accounts-CW\YE_2025.11.30\workings\_master_orders.json"
```

Expect: 95 delivered, 24 business (GBP 2013.80), 71 personal (GBP 1977.58),
zero gaps, 6 item-sum flags, exit 0.

## Validation history

Built and validated by Cedric in Session 11 (2026.07.13). Script output
reproduces the hand-built FY 2024-25 schedule exactly (see SKILL.md validation
history). The chunk pulls that feed it are done by Cedric via the
amazon-order-history MCP (v0.3.1, start_index); this script is the deterministic
build/reconcile/format stage.
