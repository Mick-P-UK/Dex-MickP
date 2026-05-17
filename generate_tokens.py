#!/usr/bin/env python3
"""
generate_tokens.py -- MCSB Phase 1.3e helper

Mints two cryptographically random 32-byte hex tokens and prints the two
lines Mick should paste into C:\\Users\\pavey\\.env.

This script does NOT write to .env itself -- per project rule the global
.env is hand-edited only and lives ONLY at C:\\Users\\pavey\\.env.

Usage:
  python generate_tokens.py
  python generate_tokens.py --bytes 48     # longer tokens
  python generate_tokens.py --rotate-mobile  # mint a new mobile token only
  python generate_tokens.py --rotate-pc      # mint a new PC token only
"""

from __future__ import annotations

import argparse
import secrets


def mint(nbytes: int) -> str:
    return secrets.token_hex(nbytes)


def main() -> None:
    ap = argparse.ArgumentParser(description="Mint MCSB bearer tokens.")
    ap.add_argument("--bytes", type=int, default=32, help="Token length in bytes (default 32 -> 64 hex chars).")
    ap.add_argument("--rotate-pc", action="store_true", help="Print only a new MCSB_PC_TOKEN line.")
    ap.add_argument("--rotate-mobile", action="store_true", help="Print only a new MCSB_MOBILE_TOKEN line.")
    args = ap.parse_args()

    print("-" * 72)
    print("MCSB token mint -- paste the line(s) below into C:\\Users\\pavey\\.env")
    print("(replace any existing MCSB_*_TOKEN lines so the file stays unique)")
    print("-" * 72)

    if args.rotate_pc:
        print(f"MCSB_PC_TOKEN={mint(args.bytes)}")
    elif args.rotate_mobile:
        print(f"MCSB_MOBILE_TOKEN={mint(args.bytes)}")
    else:
        print(f"MCSB_PC_TOKEN={mint(args.bytes)}")
        print(f"MCSB_MOBILE_TOKEN={mint(args.bytes)}")

    print("-" * 72)
    print("After saving .env, hit GET /health and confirm:")
    print('  "pc_token_configured": true')
    print('  "mobile_token_configured": true')
    print("-" * 72)


if __name__ == "__main__":
    main()
