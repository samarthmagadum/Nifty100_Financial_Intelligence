import pandas as pd

from src.database.database_utils import get_connection


def load_sectors():

    print("=" * 60)
    print("LOADING SECTORS")
    print("=" * 60)

    df = pd.read_excel("data/supporting/sectors.xlsx")

    print("\nRows :", len(df))
    print(df.head())

    connection = get_connection()

    cursor = connection.cursor()

    # Create table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sectors (

        id INTEGER PRIMARY KEY,

        company_id TEXT,

        broad_sector TEXT,

        sub_sector TEXT,

        index_weight_pct REAL,

        market_cap_category TEXT

    )
    """)

    # Clear old data
    cursor.execute("DELETE FROM sectors")

    # Insert rows
    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO sectors
        VALUES (?, ?, ?, ?, ?, ?)
        """, (

            int(row["id"]),
            row["company_id"],
            row["broad_sector"],
            row["sub_sector"],
            float(row["index_weight_pct"]),
            row["market_cap_category"]

        ))

    connection.commit()

    connection.close()

    print("\nLoaded Successfully :", len(df))


if __name__ == "__main__":

    load_sectors()