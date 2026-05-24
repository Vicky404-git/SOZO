# sozo/core/runtime.py

import os
from pathlib import Path
from dotenv import load_dotenv

# =========================================================
# GLOBAL PATHS
# =========================================================

SOZO_DIR = Path.home() / ".sozo"

DB_PATH = SOZO_DIR / "sozo.db"

VAULT_PATH = SOZO_DIR / "vault"

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

# =========================================================
# ENV
# =========================================================

load_dotenv(ENV_PATH)

# =========================================================
# HELPERS
# =========================================================

def get_groq_api_key():
    return os.getenv("GROQ_API_KEY")
