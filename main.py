#!/usr/bin/env python3

from core.database import initialize_database
from cli.app import app

def main():
    initialize_database()
    app()

if __name__ == "__main__":
    main()