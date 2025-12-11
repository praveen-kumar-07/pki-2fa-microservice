import pyotp, base64, time

def hex_to_base32(hex_seed: str) -> str:
    return base64.b32encode(bytes.fromhex(hex_seed)).decode()

def get_totp_object(hex_seed: str):
    base32_seed = hex_to_base32(hex_seed)
    # SHA-1, 30s interval, 6 digits
    return pyotp.TOTP(base32_seed, digits=6, digest='sha1', interval=30)

def generate_totp_code(hex_seed: str) -> str:
    return get_totp_object(hex_seed).now()

def verify_totp_code(hex_seed: str, code: str) -> bool:
    # +/- 1 period tolerance
    return get_totp_object(hex_seed).verify(code, valid_window=1)

def get_remaining_seconds() -> int:
    return 30 - int(time.time() % 30)