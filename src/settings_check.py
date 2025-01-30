import os
from dotenv import load_dotenv


def load_settings():
    # Load environment variables from .env file
    load_dotenv()

    PORT = int(os.getenv("SITE_PORT", 8000))
    DIRECTORY = os.getenv("SITE_PATH")

    if not DIRECTORY:
        raise ValueError("Error: SITE_PATH environment variable is not set.")

    return PORT, DIRECTORY
