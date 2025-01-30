import os
from dotenv import load_dotenv
from src.server import run_server

# Load environment variables from .env file
load_dotenv()

PORT = int(os.getenv("SITE_PORT", 8000))
DIRECTORY = os.getenv("SITE_PATH")

if not DIRECTORY:
    raise ValueError("Error: No site path is set. Either set SITE_PATH in .env or pass it as an argument via CLI.")


if __name__ == "__main__":
    run_server()
