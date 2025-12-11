#!/usr/bin/env python3
import datetime, sys, os
from app.auth_core import generate_totp_code 

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def log_message(message: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f: f.write(message + "\n")

try:
    log_message(f"[{timestamp} UTC] Cron job started.")
    
    if not os.path.exists(SEED_PATH):
        log_message(f"[{timestamp} UTC] ERROR: Seed file not found.")
        sys.exit(1)
        
    hex_seed = open(SEED_PATH, "r").read().strip()
    code = generate_totp_code(hex_seed)

    # Required Log Format
    log_message(f"{timestamp} - 2FA Code: {code}")

except Exception as e:
    log_message(f"[{timestamp} UTC] CRITICAL ERROR: {str(e)}")