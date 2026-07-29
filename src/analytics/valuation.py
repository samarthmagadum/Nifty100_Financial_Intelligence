import sqlite3
import pandas as pd
from pathlib import Path


# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(
    exist_ok=True
)


VALUATION_FILE = (
    OUTPUT_DIR /
    "valuation_summary.xlsx"
)


FLAGS_FILE = (
    OUTPUT_DIR /
    "valuation_flags.csv"
)



# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():

    return sqlite3.connect(
        str(DB_PATH)
    )



# =====================================================
# LOAD DATA
# =====================================================

def load_valuation_data():


    conn = get_connection()


    query = """

    SELECT


        c.id AS company_id,


        c.company_name,


        s.broad_sector AS sector,


        m.market_cap_crore,


        m.pe_ratio,


        m.pb_ratio,


        m.ev_ebitda,


        f.free_cash_flow_cr



    FROM companies c



    JOIN market_cap m


    ON c.id = m.company_id



    JOIN sectors s


    ON c.id = s.company_id



    JOIN financial_ratios f


    ON c.id = f.company_id



    WHERE m.year = (

        SELECT MAX(year)

        FROM market_cap

    )



    AND f.year = (

        SELECT MAX(year)

        FROM financial_ratios

    )


    """



    df = pd.read_sql(
        query,
        conn
    )


    conn.close()


    return df



# =====================================================
# CLEAN DATA
# =====================================================


def clean_data(df):


    numeric_columns = [

        "market_cap_crore",

        "pe_ratio",

        "pb_ratio",

        "ev_ebitda",

        "free_cash_flow_cr"

    ]


    for col in numeric_columns:


        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )


    df[numeric_columns] = (

        df[numeric_columns]

        .fillna(0)

    )


    return df



# =====================================================
# FCF YIELD
# =====================================================


def calculate_fcf_yield(df):


    df["FCF_yield_pct"] = (

        df["free_cash_flow_cr"]

        /

        df["market_cap_crore"]

        *

        100

    )


    df["FCF_yield_pct"] = (

        df["FCF_yield_pct"]

        .round(2)

    )


    return df



# =====================================================
# SECTOR MEDIAN PE
# =====================================================


def calculate_sector_pe(df):


    sector_median = (

        df.groupby(
            "sector"
        )

        ["pe_ratio"]

        .median()

        .reset_index()

    )


    sector_median.rename(

        columns={

            "pe_ratio":
            "5yr_median_PE"

        },

        inplace=True

    )


    df = df.merge(

        sector_median,

        on="sector",

        how="left"

    )


    return df



# =====================================================
# VALUATION FLAGS
# =====================================================


def apply_flags(df):


    def flag(row):


        pe = row["pe_ratio"]

        median = row["5yr_median_PE"]



        if median == 0:

            return "Fair"



        if pe > median * 1.5:

            return "Caution"



        elif pe < median * 0.7:

            return "Discount"



        else:

            return "Fair"



    df["flag"] = df.apply(

        flag,

        axis=1

    )



    df["PE_vs_sector_median_pct"] = (

        (

            df["pe_ratio"]

            -

            df["5yr_median_PE"]

        )

        /

        df["5yr_median_PE"]

        *

        100

    ).round(2)



    return df



# =====================================================
# SAVE OUTPUT
# =====================================================


def save_outputs(df):


    columns = [

        "company_id",

        "company_name",

        "sector",

        "pe_ratio",

        "pb_ratio",

        "ev_ebitda",

        "FCF_yield_pct",

        "5yr_median_PE",

        "PE_vs_sector_median_pct",

        "flag"

    ]



    output_df = df[columns].copy()



    output_df.rename(

        columns={

            "pe_ratio":"P/E",

            "pb_ratio":"P/B",

            "ev_ebitda":"EV/EBITDA"

        },

        inplace=True

    )



    output_df.to_excel(

        VALUATION_FILE,

        index=False

    )



    flags_df = output_df[

        output_df["flag"]

        .isin(

            [

                "Caution",

                "Discount"

            ]

        )

    ]



    flags_df.to_csv(

        FLAGS_FILE,

        index=False

    )


    print(
        "Created:",
        VALUATION_FILE
    )


    print(
        "Created:",
        FLAGS_FILE
    )



# =====================================================
# MAIN
# =====================================================


if __name__ == "__main__":


    print(
        "Loading valuation data..."
    )


    df = load_valuation_data()



    print(
        "Companies:",
        len(df)
    )



    df = clean_data(df)



    df = calculate_fcf_yield(df)



    df = calculate_sector_pe(df)



    df = apply_flags(df)



    save_outputs(df)



    print(
        "Valuation module completed"
    )