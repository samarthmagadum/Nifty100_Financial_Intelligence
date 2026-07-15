"""
test_connection.py

Purpose
-------
Tests SQLite database connection.
"""

from database_utils import get_connection, close_connection


def main():

    try:

        connection = get_connection()

        print("=" * 60)
        print("DATABASE CONNECTION SUCCESSFUL")
        print("=" * 60)

        cursor = connection.cursor()

        cursor.execute("SELECT sqlite_version();")

        version = cursor.fetchone()

        print(f"SQLite Version : {version[0]}")

        close_connection(connection)

        print("\nConnection Closed Successfully")

    except Exception as e:

        print("Database Error")

        print(e)


if __name__ == "__main__":

    main()