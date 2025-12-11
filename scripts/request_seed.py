import requests
import sys
import os

# Instructor API Endpoint
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str):
    """
    Sends the student's public key to the instructor API to receive a deterministic encrypted seed.
    """
    try:
        # Load your public key from the repository root
        with open("student_public.pem", "r") as f:
            public_key = f.read()

        payload = {
            "student_id": student_id,
            "github_repo_url": github_repo_url,
            "public_key": public_key
        }
        
        print(f"Requesting seed for Student ID: {student_id}...")

        # Send POST request
        response = requests.post(API_URL, json=payload, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        encrypted_seed = data["encrypted_seed"]
        
        # Save the encrypted seed to the root folder
        with open("encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)
            
        print("✅ Success! Encrypted seed saved to encrypted_seed.txt")
        print("REMINDER: Do NOT commit encrypted_seed.txt to Git.")

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code}. Response: {e.response.text}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Ensure the script is run from the project root directory
    if not os.path.exists("student_public.pem"):
        print("Error: Must be run from the project root directory (where student_public.pem is located).")
        sys.exit(1)
        
    if len(sys.argv) != 3:
        print("\nUsage: python scripts/request_seed.py [YOUR_STUDENT_ID] [YOUR_GITHUB_REPO_URL]")
        print("Example: python scripts/request_seed.py S12345 https://github.com/user/pki-2fa")
        sys.exit(1)
    
    request_seed(sys.argv[1], sys.argv[2])