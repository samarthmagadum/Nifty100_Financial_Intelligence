"""
create_database.py

Purpose
-------
Creates the SQLite database from schema.sql

"""

import sqlite3
from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FOLDER = PROJECT_ROOT / "db"

SCHEMA_FILE = DB_FOLDER / "schema.sql"

DATABASE_FILE = DB_FOLDER / "nifty100.db"


# ==========================================================
# Create Database
# ==========================================================

def create_database():

    print("=" * 60)
    print("Creating SQLite Database")
    print("=" * 60)

    # Connect to SQLite
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Read schema.sql
    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:

        sql_script = file.read()

    # Execute SQL Script
    cursor.executescript(sql_script)

    connection.commit()

    print("\n✅ Database Created Successfully")

    connection.close()


# ==========================================================
# Display Tables
# ==========================================================

def show_tables():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""

        SELECT name

        FROM sqlite_master

        WHERE type='table'

        ORDER BY name;

    """)

    tables = cursor.fetchall()

    print("\n" + "=" * 60)
    print("DATABASE TABLES")
    print("=" * 60)

    for table in tables:

        print("✔", table[0])

    connection.close()


# ==========================================================
# Check Foreign Keys
# ==========================================================

def check_foreign_keys():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    # Enable foreign keys for this connection
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Check status
    cursor.execute("PRAGMA foreign_keys;")

    result = cursor.fetchone()

    print("\n" + "=" * 60)
    print("FOREIGN KEY STATUS")
    print("=" * 60)

    if result[0] == 1:
        print("✅ Foreign Keys Enabled")
    else:
        print("❌ Foreign Keys Disabled")

    connection.close()


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    create_database()

    show_tables()

    check_foreign_keys()
