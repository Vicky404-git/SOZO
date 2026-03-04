#!/usr/bin/env python3

from sozo.core.database import initialize_database
from sozo.cli.app import app


def main():
    initialize_database()
    app()


if __name__ == "__main__":
    main()