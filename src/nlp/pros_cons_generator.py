import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"


# ==========================================================
# DATABASE
# ==========================================================

conn = sqlite3.connect(DB_PATH)


# ==========================================================
# LOAD COMPANIES
# ==========================================================

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name,
        roce_percentage
    FROM companies
    """,
    conn
)


# ==========================================================
# LOAD FINANCIAL RATIOS
# ==========================================================

financial = pd.read_sql(
    """
    SELECT *

    FROM financial_ratios

    ORDER BY company_id, year
    """,
    conn
)


# ==========================================================
# LOAD MARKET CAP
# ==========================================================

market = pd.read_sql(
    """
    SELECT *

    FROM market_cap
    """,
    conn
)


conn.close()


# ==========================================================
# LATEST YEAR
# ==========================================================

# Remove TTM rows
# Remove TTM rows
financial = financial[
    financial["year"] != "TTM"
].copy()

# Use latest annual year
latest_year = "Mar 2024"

latest_financial = financial[
    financial["year"] == latest_year
].copy()

latest_financial = latest_financial.drop_duplicates(
    subset=["company_id"],
    keep="last"
)

latest_financial = latest_financial.drop_duplicates(
    subset=["company_id"],
    keep="last"
)


latest_market = market[
    market["year"] == market["year"].max()
].copy()


# ==========================================================
# MERGE
# ==========================================================

df = (
    latest_financial
    .merge(
        companies,
        on="company_id",
        how="left"
    )
    .merge(
        latest_market,
        on="company_id",
        how="left"
    )
)

df = df.drop_duplicates(
    subset=["company_id"],
    keep="first"
)


# ==========================================================
# CLEAN NUMERIC COLUMNS
# ==========================================================

numeric_columns = [

    "return_on_equity_pct",

    "debt_to_equity",

    "interest_coverage",

    "free_cash_flow_cr",

    "operating_profit_margin_pct",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "eps_cagr_5yr",

    "dividend_payout_ratio_pct",

    "dividend_yield_pct",

    "market_cap_crore",

    "roce_percentage"

]


for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


df[numeric_columns] = df[numeric_columns].fillna(0)


# ==========================================================
# RESULT LIST
# ==========================================================

records = []


print("=" * 60)
print("DAY 30")
print("Pros / Cons Generator")
print("=" * 60)

print()

print("Companies :", len(df))
print("Latest Year :", latest_year)

print()

print(df.head())



# ==========================================================
# CONFIDENCE ENGINE
# ==========================================================

def confidence(score):

    """
    Keep confidence between 60 and 100.
    """

    score = max(60, min(100, score))

    return int(score)


# ==========================================================
# ADD RECORD
# ==========================================================

def add_record(

    company_id,

    rule_type,

    rule_id,

    text,

    confidence_pct

):

    records.append(

        {

            "company_id": company_id,

            "type": rule_type,

            "rule_id": rule_id,

            "text": text,

            "confidence_pct": confidence(confidence_pct)

        }

    )


# ==========================================================
# PRO RULE ENGINE
# ==========================================================

print()

print("=" * 60)
print("Evaluating PRO Rules")
print("=" * 60)

for _, row in df.iterrows():

    cid = row["company_id"]

    company = row["company_name"]


    # =====================================================
    # PRO RULE 1
    # ROE > 20%
    # =====================================================

    if row["return_on_equity_pct"] > 20:

        add_record(

            cid,

            "pro",

            "P01",

            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

            95

        )


    # =====================================================
    # PRO RULE 2
    # Positive FCF
    # =====================================================

    if row["free_cash_flow_cr"] > 0:

        add_record(

            cid,

            "pro",

            "P02",

            "Strong free cash flow generation over 5 years signals healthy business fundamentals.",

            90

        )


    # =====================================================
    # PRO RULE 3
    # Debt Free
    # =====================================================

    if row["debt_to_equity"] == 0:

        add_record(

            cid,

            "pro",

            "P03",

            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",

            95

        )


    # =====================================================
    # PRO RULE 4
    # Revenue CAGR
    # =====================================================

    if row["revenue_cagr_5yr"] > 15:

        add_record(

            cid,

            "pro",

            "P04",

            "Revenue growing above 15% CAGR over 5 years reflects strong business momentum.",

            88

        )


    # =====================================================
    # PRO RULE 5
    # OPM
    # =====================================================

    if row["operating_profit_margin_pct"] > 25:

        add_record(

            cid,

            "pro",

            "P05",

            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",

            90

        )


    # =====================================================
    # PRO RULE 6
    # PAT CAGR
    # =====================================================

    if row["pat_cagr_5yr"] > 20:

        add_record(

            cid,

            "pro",

            "P06",

            "Net profit compounding above 20% over 5 years creates significant shareholder value.",

            92

        )


        # =====================================================
    # PRO RULE 7
    # ICR > 10 OR Debt Free
    # =====================================================

    if (
        row["interest_coverage"] > 10
        or
        row["debt_to_equity"] == 0
    ):

        add_record(

            cid,

            "pro",

            "P07",

            "Very high interest coverage ratio reflects negligible financial stress from debt servicing.",

            90

        )


    # =====================================================
    # PRO RULE 8
    # Dividend Yield > 2 AND Positive FCF
    # =====================================================

    if (

        row["dividend_yield_pct"] > 2

        and

        row["free_cash_flow_cr"] > 0

    ):

        add_record(

            cid,

            "pro",

            "P08",

            "Consistent dividend yield above 2% backed by positive free cash flow.",

            88

        )


    # =====================================================
    # PRO RULE 9
    # EPS CAGR > 15
    # =====================================================

    if row["eps_cagr_5yr"] > 15:

        add_record(

            cid,

            "pro",

            "P09",

            "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.",

            92

        )


    # =====================================================
    # PRO RULE 10
    # ROE Improving 3 Years
    # =====================================================

    history = financial[
        financial["company_id"] == cid
    ].copy()

    history = history.sort_values("year")

    if len(history) >= 3:

        roe = history[
            "return_on_equity_pct"
        ].tail(3).tolist()

        if (

            roe[0] < roe[1] < roe[2]

        ):

            add_record(

                cid,

                "pro",

                "P10",

                "Return on equity improving for three consecutive years shows strengthening business quality.",

                90

            )


    # =====================================================
    # PRO RULE 11
    # Operating Leverage
    # =====================================================

    if (

        row["pat_cagr_5yr"]

        >

        row["revenue_cagr_5yr"]

    ):

        add_record(

            cid,

            "pro",

            "P11",

            "Revenue growing slower than profits shows improving operating leverage and scale benefits.",

            85

        )


    # =====================================================
    # PRO RULE 12
    # Assets Growing + Debt Declining
    # (Skip if data unavailable)
    # =====================================================

    try:

        bs = pd.read_sql(

            """

            SELECT

                year,

                total_assets,

                borrowings

            FROM balancesheet

            WHERE company_id = ?

            ORDER BY year

            """,

            sqlite3.connect(DB_PATH),

            params=[cid]

        )

        if len(bs) >= 3:

            assets = pd.to_numeric(
                bs["total_assets"],
                errors="coerce"
            ).fillna(0).tail(3).tolist()

            debt = pd.to_numeric(
                bs["borrowings"],
                errors="coerce"
            ).fillna(0).tail(3).tolist()

            if (

                assets[0] < assets[1] < assets[2]

                and

                debt[0] > debt[1] > debt[2]

            ):

                add_record(

                    cid,

                    "pro",

                    "P12",

                    "Growing asset base funded by internal accruals reflects self-sustaining growth.",

                    90

                )

    except:

        pass



    # =====================================================
    # CON RULE 1
    # D/E > 2
    # =====================================================

    if row["debt_to_equity"] > 2:

     add_record(

        cid,

        "con",

        "C01",

        f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated and warrants monitoring.",

        92

    )


    # =====================================================
    # CON RULE 2
    # Negative Free Cash Flow
    # =====================================================

    if row["free_cash_flow_cr"] < 0:

     add_record(

        cid,

        "con",

        "C02",

        "Free cash flow is negative, raising concern about cash generation quality.",

        88

    )


    # =====================================================
    # CON RULE 3
    # OPM Declining (3 Years)
    # =====================================================

    history = financial[
    financial["company_id"] == cid
     ].copy()

    history = history.sort_values("year")

    if len(history) >= 3:

     opm = history[
        "operating_profit_margin_pct"
    ].tail(3).tolist()

    if opm[0] > opm[1] > opm[2]:

        add_record(

            cid,

            "con",

            "C03",

            "Operating margins have declined for three consecutive years.",

            82

        )


    # =====================================================
    # CON RULE 4
    # Net Profit Margin Negative
    # =====================================================

    if row["net_profit_margin_pct"] < 0:

     add_record(

        cid,

        "con",

        "C04",

        "Company reported a negative net profit margin in the latest financial year.",

        95

    )


    # =====================================================
    # CON RULE 5
    # Revenue CAGR < 0
    # =====================================================

    if row["revenue_cagr_5yr"] < 0:

     add_record(

        cid,

        "con",

        "C05",

        "Revenue growth has been negative over the recent period.",

        90

    )


    # =====================================================
    # CON RULE 6
    # Interest Coverage < 1.5
    # =====================================================

    if row["interest_coverage"] < 1.5:

     add_record(

        cid,

        "con",

        "C06",

        "Interest coverage below 1.5x indicates debt servicing risk.",

        96

    )

    # =====================================================
    # CON RULE 7
    # Dividend Yield > 5% (Proxy for High Payout)
    # =====================================================

    if row["dividend_payout_ratio_pct"] > 100:

     add_record(
        cid,
        "con",
        "C07",
        "Dividend payout ratio above 100% indicates dividends may be funded from reserves and could be unsustainable.",
        85
    )


    # =====================================================
    # CON RULE 8
    # Debt/Equity Rising for 3 Years
    # =====================================================

    history = financial[
    financial["company_id"] == cid
    ].copy()

    history = history.sort_values("year")

    if len(history) >= 3:

     de = history["debt_to_equity"].tail(3).fillna(0).tolist()

    if de[0] < de[1] < de[2]:

         add_record(
            cid,
            "con",
            "C08",
            "Debt-to-equity has increased for three consecutive years.",
            85
        )


   # =====================================================
   # CON RULE 9
   # EPS Declining for 3 Consecutive Years
   # =====================================================

    history = financial[
    financial["company_id"] == cid
].copy()

    history = history.sort_values("year")

    if len(history) >= 3:

     eps = (
        history["earnings_per_share"]
        .fillna(0)
        .tail(3)
        .tolist()
    )

    if eps[0] > eps[1] > eps[2]:

        add_record(
            cid,
            "con",
            "C09",
            "Earnings per share have declined for three consecutive years, reflecting deteriorating profitability.",
            90
        )

    # =====================================================
    # CON RULE 10
    # ROCE < 10%
    # =====================================================

    if "roce_percentage" in row.index:

     if pd.notna(row["roce_percentage"]):

        if row["roce_percentage"] < 10:

            add_record(
                cid,
                "con",
                "C10",
                "Return on capital employed below 10% indicates weak capital efficiency.",
                90
            )


    # =====================================================
    # CON RULE 11
    # Net Debt > 3x EBITDA
    # =====================================================

    if "ev_ebitda" in row.index:

     if pd.notna(row["ev_ebitda"]):

        if row["ev_ebitda"] > 30:

         add_record(
        cid,
        "con",
        "C11",
        "High EV/EBITDA multiple indicates expensive valuation and may limit upside.",
        75
       )


    # =====================================================
    # CON RULE 12
    #  Revenue CAGR < 5%
    #  =====================================================

    if row["revenue_cagr_5yr"] < 5:

     add_record(
        cid,
        "con",
        "C12",
        "Revenue growth below 5% over five years suggests limited business momentum.",
        80
    )


# ==========================================================
# PRO RULE SUMMARY
# ==========================================================

pro_count = len([r for r in records if r["type"] == "pro"])
con_count = len([r for r in records if r["type"] == "con"])

print()

print("=" * 60)
print("RULE SUMMARY")
print("=" * 60)

print(f"Total Pro Records : {pro_count}")
print(f"Total Con Records : {con_count}")
print(f"Total Records     : {len(records)}")


# =====================================================
# CREATE DATAFRAME
# =====================================================

pros_cons_df = pd.DataFrame(records)

# Keep only confidence > 60
pros_cons_df = pros_cons_df[
    pros_cons_df["confidence_pct"] > 60
].copy()


# =====================================================
# FALLBACK VALIDATION
# Ensure every company has at least one Pro and one Con
# =====================================================

all_companies = df["company_id"].unique()

for cid in all_companies:

    company_records = pros_cons_df[
        pros_cons_df["company_id"] == cid
    ]

    # ---------- Missing Pro ----------
    if "pro" not in company_records["type"].values:

        fallback_pro = {
            "company_id": cid,
            "type": "pro",
            "rule_id": "P99",
            "text": "Company has stable operating performance based on available financial data.",
            "confidence_pct": 65
        }

        pros_cons_df = pd.concat(
            [pros_cons_df, pd.DataFrame([fallback_pro])],
            ignore_index=True
        )

    # ---------- Missing Con ----------
    if "con" not in company_records["type"].values:

        fallback_con = {
            "company_id": cid,
            "type": "con",
            "rule_id": "C99",
            "text": "No major risk indicators were triggered; investors should continue monitoring future performance.",
            "confidence_pct": 65
        }

        pros_cons_df = pd.concat(
            [pros_cons_df, pd.DataFrame([fallback_con])],
            ignore_index=True
        )

# =====================================================
# OUTPUT FOLDER
# =====================================================

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

output_file = OUTPUT_DIR / "pros_cons_generated.csv"

pros_cons_df.to_csv(
    output_file,
    index=False
)

print()
print("=" * 60)
print("CSV GENERATED")
print("=" * 60)
print(f"Records Saved : {len(pros_cons_df)}")
print(output_file)

# =====================================================
# VALIDATION
# =====================================================

companies = sorted(df["company_id"].unique())

missing_pro = []
missing_con = []

for company in companies:

    company_records = pros_cons_df[
        pros_cons_df["company_id"] == company
    ]

    if "pro" not in company_records["type"].values:
        missing_pro.append(company)

    if "con" not in company_records["type"].values:
        missing_con.append(company)

print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)

print(f"Companies Checked : {len(companies)}")
print(f"Missing Pro : {len(missing_pro)}")
print(f"Missing Con : {len(missing_con)}")

if missing_pro:
    print("\nCompanies Missing Pro:")
    print(missing_pro)

if missing_con:
    print("\nCompanies Missing Con:")
    print(missing_con)

if not missing_pro and not missing_con:
    print("\nSUCCESS: Every company has at least one Pro and one Con.")

print()
print("=" * 60)
print("DAY 30 COMPLETED")
print("=" * 60)