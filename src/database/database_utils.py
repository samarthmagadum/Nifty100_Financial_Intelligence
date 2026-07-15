"""
database_utils.py

Purpose
-------
Provides helper functions for connecting to the SQLite database.

"""

import sqlite3
from pathlib import Path


# ==========================================================
# Database Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_FILE = PROJECT_ROOT / "db" / "nifty100.db"


# ==========================================================
# Get Database Connection
# ==========================================================

def get_connection():
    """
    Creates and returns a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    # Enable Foreign Keys
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection


# ==========================================================
# Close Database Connection
# ==========================================================

def close_connection(connection):
    """
    Safely closes the database connection.
    """

    if connection:
        connection.close()