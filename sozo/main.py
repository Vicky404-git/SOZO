#!/usr/bin/env python3

from sozo.core.database import initialize_database
from sozo.core.config import DB_PATH
from sozo.cli.app import app

def main():
    # Only run the heavy migrations if this is a fresh install!
    if not DB_PATH.exists():
        initialize_database()
        
    app()

if __name__ == "__main__":
    main()