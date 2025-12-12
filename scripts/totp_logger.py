#!/usr/bin/env python3
import datetime
import sys
import os
from app.auth_core import generate_totp_code # Imports auth_core successfully

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

try:
    if not os.path.exists(SEED_PATH):
        # We redirect this error to stderr via cron job command, so we just exit
        sys.exit(1)
        
    hex_seed = open(SEED_PATH, "r").read().strip()
    code = generate_totp_code(hex_seed)

    # Print the output to stdout/cron log
    print(f"{timestamp} - 2FA Code: {code}")

except Exception as e:
    # Print errors to stderr, which the cron job redirects to the log file
    print(f"CRITICAL ERROR: {str(e)}", file=sys.stderr)