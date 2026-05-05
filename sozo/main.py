#!/usr/bin/env python3

from sozo.core.database import initialize_database
from sozo.cli.app import app

# ALWAYS run - it's idempotent and prevents the crash on update
initialize_database()

def main():
    """This is the entry point that setup.py is looking for!"""
    app()

if __name__ == "__main__":
    main()
