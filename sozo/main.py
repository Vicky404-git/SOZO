#!/usr/bin/env python3

from sozo.core.database import initialize_database
from sozo.core.runtime import SOZO_DIR, VAULT_PATH, DB_PATH
from sozo.cli.app import app


def main():
    SOZO_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    initialize_database()   # ← no if check
    app()


if __name__ == "__main__":
    main()
