"""
validator.py

Sprint 1 - Day 3
Data Quality Validation


"""

# ==========================================================
# Import Required Libraries
# ==========================================================

import pandas as pd
from pathlib import Path

# Import Loader Functions
from loader import (
    load_core_files,
    load_supporting_files
)

# ==========================================================
# Output Folder
# ==========================================================

OUTPUT_DIR = Path("../../output")
OUTPUT_DIR.mkdir(exist_ok=True)

VALIDATION_FILE = OUTPUT_DIR / "validation_failures.csv"

# Store all validation issues
validation_results = []

# ==========================================================
# Helper Function
# ==========================================================

def add_failure(rule,
                dataset,
                severity,
                message,
                row=None):
    """
    Store validation failures.

    Parameters
    ----------
    rule : DQ Rule Name
    dataset : Dataset Name
    severity : CRITICAL / WARNING
    message : Error Description
    row : Row Number
    """

    validation_results.append({

        "Rule": rule,
        "Dataset": dataset,
        "Severity": severity,
        "Row": row,
        "Message": message

    })


# ==========================================================
# Normalize Company IDs
# ==========================================================

def normalize_company_id(series):
    """
    Clean company IDs before comparison.

    Example

    abb
    ABB
    ABB

    becomes

    ABB
    ABB
    ABB
    """

    return (

        series.astype(str)
              .str.strip()
              .str.upper()

    )

# ==========================================================
# Debug Company IDs
# ==========================================================

def debug_company_ids(core):
    """
    Display company IDs that exist in child tables
    but are missing from the companies table.
    """

    companies = set(
        normalize_company_id(core["companies"]["id"])
    )

    pnl = set(
        normalize_company_id(core["profitandloss"]["company_id"])
    )

    missing = sorted(pnl - companies)

    print("\n" + "=" * 60)
    print("Company IDs Missing in Companies Table")
    print("=" * 60)

    for item in missing:
        print(item)

    print("=" * 60)

def debug_duplicates(pl, company_name):
    """
    Display duplicate rows for one company.
    """

    duplicate_rows = pl[
        pl["company_id"] == company_name
    ]

    print("\n")
    print("=" * 80)
    print(company_name)
    print("=" * 80)

    print(duplicate_rows)


# ==========================================================
# DQ-01
# Primary Key Validation
# Companies.id must be unique
# ==========================================================

def dq01_company_id_unique(companies):

    print("Running DQ-01...")

    duplicates = companies[
        companies["id"].duplicated(keep=False)
    ]

    if duplicates.empty:

        print("✔ DQ-01 Passed")

        return

    for index, row in duplicates.iterrows():

        add_failure(

            "DQ-01",
            "companies",
            "CRITICAL",
            f"Duplicate company id : {row['id']}",
            index

        )

    print(f"✘ DQ-01 Failed : {len(duplicates)} records")


# ==========================================================
# DQ-02
# company_id + year must be unique
# ==========================================================

def dq02_company_year_unique(pl):

    print("Running DQ-02...")

    temp = pl.copy()

    temp["company_id"] = normalize_company_id(
        temp["company_id"]
    )

    temp["year"] = temp["year"].astype(str).str.strip()

    duplicates = temp[
        temp.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    if duplicates.empty:

        print("✔ DQ-02 Passed")

        return

    for index, row in duplicates.iterrows():

        add_failure(

            "DQ-02",
            "profitandloss",
            "CRITICAL",
            f"Duplicate company/year : {row['company_id']} - {row['year']}",
            index

        )

    print(f"✘ DQ-02 Failed : {len(duplicates)} records")


# ==========================================================
# DQ-03
# Foreign Key Validation
# ==========================================================



def dq03_foreign_key(core):

    print("Running DQ-03...")

    company_ids = set(

        normalize_company_id(
            core["companies"]["id"]
        )

    )

    print("\n========== Companies IDs ==========")
    print(sorted(company_ids))

    child_tables = [

        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons"

    ]

    total_errors = 0

    for table in child_tables:

        df = core[table].copy()

        df["company_id"] = normalize_company_id(
            df["company_id"]
        )

        invalid = df[
            ~df["company_id"].isin(company_ids)
        ]

        if not invalid.empty:
           print(f"\nMissing company IDs in {table}:")
           print(invalid[["company_id", "year"]])   

        total_errors += len(invalid)

        for index, row in invalid.iterrows():

            add_failure(

                "DQ-03",
                table,
                "CRITICAL",
                f"Invalid company_id : {row['company_id']}",
                index

            )

    if total_errors == 0:

        print("✔ DQ-03 Passed")

    else:

        print(f"✘ DQ-03 Failed : {total_errors} records")


# ==========================================================
# DQ-04
# Balance Sheet Validation
# ==========================================================

def dq04_balance_sheet(bs):

    print("Running DQ-04...")

    invalid = bs[
        bs["total_assets"] <
        bs["total_liabilities"]
    ]

    if invalid.empty:

        print("✔ DQ-04 Passed")

        return

    for index, row in invalid.iterrows():

        add_failure(

            "DQ-04",
            "balancesheet",
            "WARNING",
            "Assets less than liabilities",
            index

        )

    print(f"✘ DQ-04 Failed : {len(invalid)} records")


# ==========================================================
# DQ-05
# Operating Profit Margin Validation
# ==========================================================
# Companies where OPM validation is not applicable
FINANCIAL_COMPANIES = {
    "AXISBANK",
    "HDFCBANK",
    "ICICIBANK",
    "KOTAKBANK",
    "SBIN",
    "BANKBARODA",
    "CANBK",
    "PNB",
    "UNIONBANK",
    "INDUSINDBK",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BAJAJHLDNG",
    "CHOLAFIN",
    "PFC",
    "RECLTD",
    "IRFC",
    "LICI",
    "SBILIFE",
    "HDFCLIFE",
    "ICICIPRULI",
    "ICICIGI",
    "JIOFIN",
    "SHRIRAMFIN"
}
def dq05_opm(pl):

    print("Running DQ-05...")

    temp = pl.copy()

    # Skip financial companies
    temp = temp[
        ~temp["company_id"].isin(FINANCIAL_COMPANIES)
    ]

    # Remove rows with missing values
    temp = temp.dropna(
    subset=[
        "sales",
        "operating_profit",
        "opm_percentage"
    ]
 )

    # Sales should be greater than zero
    temp = temp[
     temp["sales"] > 0
      ]

    calculated = (

        temp["operating_profit"]
        /
        temp["sales"]

    ) * 100

    difference = (

        calculated
        -
        temp["opm_percentage"]

    ).abs()

    invalid = temp[
     difference > 5
     ]
    
    print("\n========== DQ-05 Invalid Rows ==========")

    print("\nRemaining DQ-05 Companies:")
    print(sorted(invalid["company_id"].unique()))

    if invalid.empty:

        print("✔ DQ-05 Passed")

        return

    for index, row in invalid.iterrows():

        add_failure(

            "DQ-05",
            "profitandloss",
            "WARNING",
            "Operating Profit Margin mismatch",
            index

        )

    print(f"✘ DQ-05 Failed : {len(invalid)} records")

# ==========================================================
# DQ-06
# Sales should be greater than zero
# ==========================================================

def dq06_positive_sales(pl):

    print("Running DQ-06...")

    invalid = pl[pl["sales"] <= 0]

    print("\nDQ-06 Invalid Rows")
    print(invalid)

    if invalid.empty:
        print("✔ DQ-06 Passed")
        return

    for index, row in invalid.iterrows():

        add_failure(
            "DQ-06",
            "profitandloss",
            "CRITICAL",
            f"Invalid Sales : {row['sales']}",
            index
        )

    print(f"✘ DQ-06 Failed : {len(invalid)} records")

# ==========================================================
# DQ-07
# Total Assets should be positive
# ==========================================================

def dq07_positive_assets(bs):

    print("Running DQ-07...")

    invalid = bs[bs["total_assets"] <= 0]

    print("\nDQ-07 Invalid Rows")
    print(invalid)

    if invalid.empty:
        print("✔ DQ-07 Passed")
        return

    for index, row in invalid.iterrows():

        add_failure(
            "DQ-07",
            "balancesheet",
            "CRITICAL",
            f"Invalid Total Assets : {row['total_assets']}",
            index
        )

    print(f"✘ DQ-07 Failed : {len(invalid)} records")

# ==========================================================
# DQ-08
# Net Cash Flow Validation
# ==========================================================

def dq08_cashflow(cf):

    print("Running DQ-08...")

    calculated = (
        cf["operating_activity"]
        + cf["investing_activity"]
        + cf["financing_activity"]
    )

    difference = (calculated - cf["net_cash_flow"]).abs()
    invalid = cf[difference > 1]

    print("\nDQ-08 Debug")

    for index, row in invalid.iterrows():

     calculated = (
        row["operating_activity"]
        + row["investing_activity"]
        + row["financing_activity"]
        )

    print(f"Company : {row['company_id']}")
    print(f"Year    : {row['year']}")
    print(f"Calculated Net Cash Flow : {calculated}")
    print(f"Dataset Net Cash Flow    : {row['net_cash_flow']}")

    print("\nDQ-08 Invalid Rows")
    print(invalid)

    if invalid.empty:
        print("✔ DQ-08 Passed")
        return

    for index, row in invalid.iterrows():

        add_failure(
            "DQ-08",
            "cashflow",
            "WARNING",
            "Net Cash Flow mismatch",
            index
        )

    print(f"✘ DQ-08 Failed : {len(invalid)} records")

# ==========================================================
# DQ-09
# Tax Percentage between 0 and 100
# ==========================================================

def dq09_tax_percentage(pl):

    print("Running DQ-09...")

    invalid = pl[
     (pl["tax_percentage"] < -100) |
     (pl["tax_percentage"] > 200)
        ]

    if invalid.empty:
        print("✔ DQ-09 Passed")
        return

    for index, row in invalid.iterrows():

        add_failure(
            "DQ-09",
            "profitandloss",
            "WARNING",
            f"Invalid Tax Percentage : {row['tax_percentage']}",
            index
        )

    print(f"✘ DQ-09 Failed : {len(invalid)} records")

# ==========================================================
# DQ-10
# Dividend Payout should not be negative
# ==========================================================

def dq10_dividend(pl):

    print("Running DQ-10...")

    temp = pl.dropna(subset=["dividend_payout"])

    invalid = temp[temp["dividend_payout"] < 0]

    print("\n========== DQ-10 Invalid Rows ==========")
    print(
        invalid[
            [
                "company_id",
                "year",
                "net_profit",
                "dividend_payout"
            ]
        ]
    )

    if invalid.empty:
        print("✔ DQ-10 Passed")
        return

    for index, row in invalid.iterrows():

        add_failure(
            "DQ-10",
            "profitandloss",
            "WARNING",
            f"Negative Dividend : {row['dividend_payout']}",
            index
        )

    print(f"✘ DQ-10 Failed : {len(invalid)} records")

# ==========================================================
# Save Validation Report
# ==========================================================

def save_report():

    df = pd.DataFrame(validation_results)

    df.to_csv(
        VALIDATION_FILE,
        index=False
    )

    print("\nValidation Report Saved")
    print(VALIDATION_FILE)

# ==========================================================
# Main Function
# ==========================================================

def main():

    print("=" * 60)
    print("Loading datasets...")
    print("=" * 60)

    core = load_core_files()
    support = load_supporting_files()

  # -------------------------------------------------
  # Debug Company IDs
  # -------------------------------------------------

    debug_company_ids(core)

    debug_duplicates(
    core["profitandloss"],
    "ADANIPORTS"
    )

    print("\nRunning Data Quality Rules...\n")

    dq01_company_id_unique(core["companies"])
    dq02_company_year_unique(core["profitandloss"])
    dq03_foreign_key(core)
    dq04_balance_sheet(core["balancesheet"])
    dq05_opm(core["profitandloss"])

    dq06_positive_sales(core["profitandloss"])
    dq07_positive_assets(core["balancesheet"])
    dq08_cashflow(core["cashflow"])
    dq09_tax_percentage(core["profitandloss"])
    dq10_dividend(core["profitandloss"])

    save_report()

    print("\n" + "=" * 60)
    print("Validation Completed")
    print("=" * 60)

    print(f"Total Issues Found : {len(validation_results)}")


# ==========================================================
# Run Program
# ==========================================================

if __name__ == "__main__":
    main()