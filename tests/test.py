from datetime import datetime, timezone
import hmac
import hashlib
import requests
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv(".env"))

# Get the shared secret from environment variables
SHARED_SECRET = os.getenv("API_SHARED_SECRET")
if not SHARED_SECRET:
    raise ValueError("API_SHARED_SECRET environment variable is not set")

def get_utc_timestamp() -> str:
    """Get current UTC timestamp in seconds."""
    return str(int(datetime.now(timezone.utc).timestamp()))

def generate_signature(timestamp: str, method: str, path: str, body: str = ''):
    payload = f"{timestamp}:{method}:{path}"
    if body:
        payload += f":{body}"

    return hmac.new(
        SHARED_SECRET.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

# Example request
timestamp = get_utc_timestamp()
method = 'GET'
path = '/api/v1/secure-endpoint'
body = ''  # Add body for POST/PUT requests

signature = generate_signature(timestamp, method, path, body)

headers = {
    'X-Timestamp': timestamp,
    'X-Signature': signature
}

response = requests.get(
    'https://competitor-hunt-api-production.up.railway.app/api/v1/secure-endpoint',
    headers=headers
)
print(response.json())
print(headers)