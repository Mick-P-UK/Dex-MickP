---
title: Quick Start - Run EOM Portfolio Posts in Claude Code
tags:
  - SOP
  - quick-start
type: quick-start
status: active
version: 1.0
created: 2026-07-09
owner: Mick
related: SOP - End-of-Month Portfolio Posting.md
---

# Quick Start - Run the End-of-Month Portfolio Posts in Claude Code

The easy, on-demand way to create the four monthly portfolio drafts on diy-investors.com.
One sentence, no scripts. Runs locally in Claude Code so it reaches C:\Users\pavey\.env
directly. Full detail lives in "SOP - End-of-Month Portfolio Posting.md".

## Before you start (once per month)

1. Save the month-end and transactions screenshots into the four portfolio folders under
   C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\
   (the routine reads the values straight off these images, so they must exist first).
2. Make sure your PC is on. Claude Code runs on the machine, so it does not need the
   cloud - but it does need the PC awake.

## One-time setup (only the first time)

1. Install Claude Code and sign in (Anthropic account). It only needs doing once.
2. Confirm C:\Users\pavey\.env still holds the Poster Pete WordPress credentials.

## To run it

1. Open a terminal (PowerShell) and change to the vault:
   cd "C:\Vaults\Mick's-Dex-2nd-Brain"
2. Start Claude Code:
   claude
3. Type the trigger, filling in the month and post date, for example:
   run the end-of-month portfolio posts for June, all four portfolios, post date 9 July
4. The first time, Claude Code will ask permission to read C:\Users\pavey\.env and the
   DIY - Portfolios folder. Choose "always allow" so it does not ask again.
5. Let it run. When it finishes it prints four wp-admin edit URLs.
6. Open each URL, check the preview, and publish manually when you are happy.

## What Cedric does automatically in the run

- Reads the eight screenshots (values, per-stock returns, transactions, cash balances).
- Fetches the FTSE All-Share and S&P 500 month-end closes from Yahoo Finance.
- Runs every calculation in Python (never mental arithmetic).
- Updates the Indices Monthly Performance DRAFT spreadsheet (you do NOT do this by hand).
- Uploads the eight images to WordPress and builds the four posts in your house style.
- Creates all four as DRAFTS with the correct category and portfolio tag.

## Safety

- Posts are ALWAYS created as drafts. Nothing is ever auto-published.
- Credentials are read fresh from .env at run time and are never copied, logged, or hardcoded.
- Do NOT run the end-to-end job from Cowork or any cloud session: since 7 July 2026 those run
  remotely and cannot reach .env at the home-folder root. Claude Code local is the supported way.
