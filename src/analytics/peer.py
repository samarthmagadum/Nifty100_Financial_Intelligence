import pandas as pd
import sqlite3

from src.database.database_utils import get_connection

def load_peer_data():

    print()
    print("=" * 60)
    print("LOADING PEER DATA")
    print("=" * 60)

    conn = get_connection()

    query = """
    SELECT
        f.company_id,
        f.year,
        s.broad_sector,

        f.return_on_equity_pct,
        f.net_profit_margin_pct,
        f.debt_to_equity,
        f.free_cash_flow_cr,
        f.revenue_cagr_5yr,
        f.pat_cagr_5yr,
        f.interest_coverage,
        f.asset_turnover

    FROM financial_ratios f

    LEFT JOIN sectors s
    ON f.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("Rows :", len(df))

    return df


def calculate_peer_percentiles(df):

    print()
    print("=" * 60)
    print("CALCULATING PEER PERCENTILES")
    print("=" * 60)

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "interest_coverage",
        "asset_turnover"
    ]

    result = df.copy()

    for metric in metrics:

        if metric == "debt_to_equity":

            result[metric + "_percentile"] = (
                result.groupby("broad_sector")[metric]
                .rank(pct=True, ascending=False) * 100
            )

        else:

            result[metric + "_percentile"] = (
                result.groupby("broad_sector")[metric]
                .rank(pct=True) * 100
            )

    return result

def create_peer_percentiles_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    DROP TABLE IF EXISTS peer_percentiles
    """)

    cursor.execute("""
    CREATE TABLE peer_percentiles (

        company_id TEXT,

        year TEXT,

        broad_sector TEXT,

        metric TEXT,

        value REAL,

        percentile_rank REAL

    )
    """)

    conn.commit()

    print()
    print("=" * 60)
    print("PEER_PERCENTILES TABLE CREATED")
    print("=" * 60)

def save_peer_percentiles(df):

    print()
    print("=" * 60)
    print("SAVING PEER PERCENTILES")
    print("=" * 60)

    conn = get_connection()

    create_peer_percentiles_table(conn)

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "interest_coverage",
        "asset_turnover"
    ]

    rows = []

    for _, row in df.iterrows():

        for metric in metrics:

            rows.append(

                (
                    row["company_id"],
                    row["year"],
                    row["broad_sector"],
                    metric,
                    row[metric],
                    row[metric + "_percentile"]
                )

            )

    conn.executemany("""

    INSERT INTO peer_percentiles

    VALUES (?, ?, ?, ?, ?, ?)

    """, rows)

    conn.commit()

    conn.close()

    print("Rows Inserted :", len(rows))

def verify_peer_percentiles():

    print()
    print("=" * 60)
    print("VERIFYING PEER_PERCENTILES TABLE")
    print("=" * 60)

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_percentiles
    LIMIT 20
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print(df)

    print()
    print("Total Records :", len(df))

if __name__ == "__main__":

    df = load_peer_data()

    peer_df = calculate_peer_percentiles(df)

    save_peer_percentiles(peer_df)

    verify_peer_percentiles()
    
    print()
    print(peer_df.head())