import os
from pathlib import Path
from dotenv import load_dotenv

# Global Paths
SOZO_DIR = Path.home() / ".sozo"
DB_PATH = SOZO_DIR / "sozo.db"
VAULT_PATH = SOZO_DIR / "vault"

# Dynamically point to the root of the SOZO project folder for .env
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(ENV_PATH)

def get_groq_api_key():
    return os.getenv("GROQ_API_KEY")