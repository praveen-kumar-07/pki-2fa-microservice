from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair():
    # Generate RSA 4096-bit key pair with public exponent 65537 (standard)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    public_key = private_key.public_key()
    
    # Serialize private key to PEM format (PKCS8, no encryption)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save keys to the project root
    with open("student_private.pem", "wb") as f:
        f.write(private_pem)
    with open("student_public.pem", "wb") as f:
        f.write(public_pem)

if __name__ == "__main__":
    generate_rsa_keypair()
    print("✅ Student key pair generated: student_private.pem & student_public.pem")