"""
load_database.py

Purpose
-------
Loads all datasets into SQLite database.


"""

from src.database.database_utils import get_connection, close_connection
from src.etl.loader import load_core_files, load_supporting_files


# ==========================================================
# Generic Loader
# ==========================================================

def load_table(connection, dataframe, table_name, columns):

    cursor = connection.cursor()

    print(f"\nLoading {table_name}...")

    # Delete previous records
    cursor.execute(f"DELETE FROM {table_name}")

    placeholders = ", ".join(["?"] * len(columns))
    column_names = ", ".join(columns)

    query = f"""
        INSERT INTO {table_name}
        ({column_names})
        VALUES ({placeholders})
    """

    inserted = 0

    for index, row in dataframe.iterrows():

        values = [row[col] for col in columns]

        try:

            cursor.execute(query, values)
            inserted += 1

        except Exception as e:

            print("\n" + "=" * 70)
            print("ERROR INSERTING RECORD")
            print("=" * 70)

            print("Table :", table_name)
            print("Row   :", index)

            print("\nRecord:")
            print(row)

            print("\nError:")
            print(e)

            raise

    connection.commit()

    print(f"✅ {table_name} Loaded : {inserted} rows")


# ==========================================================
# Load All Tables
# ==========================================================

def load_all_tables():

    print("=" * 60)
    print("LOADING ALL TABLES")
    print("=" * 60)

    core_data = load_core_files()
    supporting_data = load_supporting_files()

    connection = get_connection()

    # Disable FK during load
    connection.execute("PRAGMA foreign_keys = OFF;")

    print("\n⚠ Foreign Keys Temporarily Disabled")

    # =====================================================
    # Companies
    # =====================================================

    load_table(
        connection,
        core_data["companies"],
        "companies",
        core_data["companies"].columns.tolist()
    )

    # =====================================================
    # Profit & Loss
    # =====================================================

    load_table(
        connection,
        core_data["profitandloss"],
        "profitandloss",
        core_data["profitandloss"].columns.tolist()
    )

    # =====================================================
    # Balance Sheet
    # =====================================================

    load_table(
        connection,
        core_data["balancesheet"],
        "balancesheet",
        core_data["balancesheet"].columns.tolist()
    )

    # =====================================================
    # Cash Flow
    # =====================================================

    load_table(
        connection,
        core_data["cashflow"],
        "cashflow",
        core_data["cashflow"].columns.tolist()
    )

    # =====================================================
    # Analysis
    # =====================================================

    load_table(
        connection,
        core_data["analysis"],
        "analysis",
        core_data["analysis"].columns.tolist()
    )

    # =====================================================
    # Documents
    # =====================================================

    load_table(
        connection,
        core_data["documents"],
        "documents",
        core_data["documents"].columns.tolist()
    )

    # =====================================================
    # Pros & Cons
    # =====================================================

    load_table(
        connection,
        core_data["prosandcons"],
        "prosandcons",
        core_data["prosandcons"].columns.tolist()
    )

    # =====================================================
    # Financial Ratios
    # =====================================================

    load_table(
        connection,
        supporting_data["financial_ratios"],
        "financial_ratios",
        supporting_data["financial_ratios"].columns.tolist()
    )

    # =====================================================
    # Market Cap
    # =====================================================

    load_table(
        connection,
        supporting_data["market_cap"],
        "market_cap",
        supporting_data["market_cap"].columns.tolist()
    )

    # =====================================================
    # Stock Prices
    # =====================================================

    load_table(
        connection,
        supporting_data["stock_prices"],
        "stock_prices",
        supporting_data["stock_prices"].columns.tolist()
    )

    # Enable FK again
    connection.execute("PRAGMA foreign_keys = ON;")

    print("\n✅ Foreign Keys Enabled")

    close_connection(connection)

    print("\n" + "=" * 60)
    print("ALL TABLES LOADED SUCCESSFULLY")
    print("=" * 60)


# ==========================================================
# Main
# ==========================================================

def main():

    load_all_tables()


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    main()