import sqlite3
import pandas as pd
import re
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(DB_PATH)

# =====================================================
# LOAD ANALYSIS TABLE
# =====================================================

analysis_df = pd.read_sql(
    """
    SELECT
        company_id,
        compounded_sales_growth,
        compounded_profit_growth,
        stock_price_cagr,
        roe
    FROM analysis
    """,
    conn,
)

# =====================================================
# REGEX PATTERN
# =====================================================

pattern = re.compile(r"(\d+)\s*Years?:?\s*([\d.]+)%", re.IGNORECASE)

# =====================================================
# PARSE TEXT FIELDS
# =====================================================

parsed_rows = []

failed_rows = []

metric_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for _, row in analysis_df.iterrows():

    company = row["company_id"]

    for metric in metric_columns:

        value = row[metric]

        if pd.isna(value):

            failed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "original_text": None,
                }
            )

            continue

        text = str(value)

        match = pattern.search(text)

        if match:

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": int(match.group(1)),
                    "value_pct": float(match.group(2)),
                }
            )

        else:

            failed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "original_text": text,
                }
            )

# =====================================================
# SAVE PARSED DATA
# =====================================================

parsed_df = pd.DataFrame(parsed_rows)

parsed_file = OUTPUT_DIR / "analysis_parsed.csv"

parsed_df.to_csv(parsed_file, index=False)

# =====================================================
# SAVE PARSE FAILURES
# =====================================================

failed_df = pd.DataFrame(failed_rows)

failed_file = OUTPUT_DIR / "parse_failures.csv"

failed_df.to_csv(failed_file, index=False)

# =====================================================
# LOAD FINANCIAL RATIOS
# =====================================================

ratio_df = pd.read_sql(
    """
    SELECT
        company_id,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        return_on_equity_pct
    FROM financial_ratios
    WHERE year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    """,
    conn,
)

conn.close()

# =====================================================
# MAP NLP METRICS TO RATIO ENGINE
# =====================================================

mapping = {
    "compounded_sales_growth": "revenue_cagr_5yr",
    "compounded_profit_growth": "pat_cagr_5yr",
    "roe": "return_on_equity_pct",
}

review_rows = []

for _, row in parsed_df.iterrows():

    metric = row["metric_type"]

    if metric not in mapping:
        continue

    company = row["company_id"]

    ratio_row = ratio_df[
        ratio_df["company_id"] == company
    ]

    if ratio_row.empty:
        continue

    ratio_value = ratio_row.iloc[0][mapping[metric]]

    if pd.isna(ratio_value):
        continue

    parsed_value = row["value_pct"]

    difference = abs(parsed_value - ratio_value)

    if difference > 5:

        review_rows.append(
            {
                "company_id": company,
                "metric": metric,
                "parsed_value": parsed_value,
                "ratio_engine_value": ratio_value,
                "difference": round(difference, 2),
                "status": "Manual Review",
            }
        )

# =====================================================
# SAVE VALIDATION REVIEW
# =====================================================

review_df = pd.DataFrame(review_rows)

review_file = OUTPUT_DIR / "validation_review.csv"

review_df.to_csv(review_file, index=False)

# =====================================================
# SUMMARY
# =====================================================

print("=" * 60)

print("NLP PARSER COMPLETED")

print("=" * 60)

print(f"Analysis records : {len(analysis_df)}")

print(f"Parsed values    : {len(parsed_df)}")

print(f"Parse failures   : {len(failed_df)}")

print(f"Validation flags : {len(review_df)}")

print()

print("Files Generated:")

print(parsed_file)

print(failed_file)

print(review_file)

print("=" * 60)