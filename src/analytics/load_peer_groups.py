import pandas as pd

from src.database.database_utils import get_connection


def load_peer_groups():

    print()
    print("=" * 60)
    print("LOADING PEER GROUPS")
    print("=" * 60)

    df = pd.read_excel(
        "data/supporting/peer_groups.xlsx"
    )

    conn = get_connection()

    df.to_sql(
        "peer_groups",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print()
    print("Rows :", len(df))
    print("peer_groups table created successfully.")


if __name__ == "__main__":

    load_peer_groups()