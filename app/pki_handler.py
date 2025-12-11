import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    try: ciphertext = base64.b64decode(encrypted_seed_b64)
    except Exception: raise ValueError("Encrypted seed is not valid Base64.")
    
    # RSA/OAEP-SHA256 decryption
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    hex_seed = plaintext.decode("utf-8")
    if len(hex_seed) != 64 or not all(c in "0123456789abcdefABCDEF" for c in hex_seed):
        raise ValueError("Decrypted data is not a valid 64-character hex seed.")
    return hex_seed.lower()