import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

url = os.environ.get("VITE_SUPABASE_URL")
key = os.environ.get("VITE_SUPABASE_ANON_KEY")

if not url or not key:
    print("Missing credentials")
    sys.exit(1)

supabase: Client = create_client(url, key)

try:
    res = supabase.auth.sign_up({
        "email": "deepal.anu.com@gmail.com",
        "password": "757498798@123"
    })
    print("Successfully signed up:")
    print(res)
except Exception as e:
    print(f"Error: {e}")
