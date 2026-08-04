"""
cashflow_kpis.py

Sprint 2 - Day 11
Cash Flow KPI Functions
"""

import sqlite3
import pandas as pd
from pathlib import Path


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================================
# Free Cash Flow (FCF)
# ==========================================================

def calculate_free_cash_flow(
        operating_activity,
        investing_activity):
    """
    Calculate Free Cash Flow.

    Formula
    -------
    Operating Activity + Investing Activity
    """

    operating_activity = operating_activity or 0
    investing_activity = investing_activity or 0

    fcf = operating_activity + investing_activity

    return round(fcf, 2)


# ==========================================================
# CFO Quality Score
# ==========================================================

def calculate_cfo_quality_score(
        cfo_values,
        pat_values):
    """
    Calculate CFO Quality Score.

    Parameters
    ----------
    cfo_values : list

    pat_values : list

    Returns
    -------
    (average_ratio, label)
    """

    ratios = []

    # Compare CFO and PAT year by year
    for cfo, pat in zip(cfo_values, pat_values):

        # Skip invalid years
        if pat == 0 or pat is None:
            continue

        ratios.append(cfo / pat)

    # No valid ratios
    if len(ratios) == 0:
        return None, "NO_DATA"

    average_ratio = sum(ratios) / len(ratios)

    if average_ratio > 1:
        label = "High Quality"

    elif average_ratio >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return round(average_ratio, 2), label


# ==========================================================
# CapEx Intensity
# ==========================================================

def calculate_capex_intensity(
        investing_activity,
        sales):
    """
    Calculate CapEx Intensity.

    Formula
    -------
    abs(Investing Activity) / Sales × 100
    """

    investing_activity = investing_activity or 0
    sales = sales or 0

    if sales == 0:
        return None, "NO_DATA"

    intensity = (abs(investing_activity) / sales) * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(intensity, 2), label


# ==========================================================
# FCF Conversion Rate
# ==========================================================

def calculate_fcf_conversion_rate(
        free_cash_flow,
        operating_profit):
    """
    Calculate FCF Conversion Rate.

    Formula
    -------
    FCF / Operating Profit × 100
    """

    free_cash_flow = free_cash_flow or 0
    operating_profit = operating_profit or 0

    if operating_profit == 0:
        return None

    conversion = (free_cash_flow / operating_profit) * 100

    return round(conversion, 2)


# ==========================================================
# Capital Allocation Pattern
# ==========================================================

def classify_capital_allocation(
        operating_activity,
        investing_activity,
        financing_activity,
        cfo_quality=None):
    """
    Classify capital allocation pattern.

    Returns
    -------
    Pattern Label
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    # (+,-,-)
    if cfo == "+" and cfi == "-" and cff == "-":

        if cfo_quality is not None and cfo_quality > 1:
            return "Shareholder Returns"

        return "Reinvestor"

    # (+,+,-)
    if cfo == "+" and cfi == "+" and cff == "-":
        return "Liquidating Assets"

    # (-,+,+)
    if cfo == "-" and cfi == "+" and cff == "+":
        return "Distress Signal"

    # (-,-,+)
    if cfo == "-" and cfi == "-" and cff == "+":
        return "Growth Funded by Debt"

    # (+,+,+)
    if cfo == "+" and cfi == "+" and cff == "+":
        return "Cash Accumulator"

    # (-,-,-)
    if cfo == "-" and cfi == "-" and cff == "-":
        return "Pre-Revenue"

    # (+,-,+)
    if cfo == "+" and cfi == "-" and cff == "+":
        return "Mixed"

    return "Other"


# ==========================================================
# FCF CAGR (5 Years)
# ==========================================================

def calculate_fcf_cagr(fcf_values):
    """
    Calculate 5-year CAGR of Free Cash Flow.

    Returns None if CAGR cannot be calculated safely.
    """

    values = [v for v in fcf_values if pd.notna(v)]

    if len(values) < 2:
        return None

    start = values[0]
    end = values[-1]

    years = len(values) - 1

    if years <= 0:
        return None

    # CAGR is not meaningful when either value is non-positive
    if start <= 0 or end <= 0:
        return None

    try:
        cagr = ((end / start) ** (1 / years) - 1) * 100
        return round(float(cagr), 2)
    except Exception:
        return None



# ==========================================================
# Deleveraging Detection
# ==========================================================

def detect_deleveraging(
        financing_activity,
        previous_borrowings,
        current_borrowings):
    """
    Deleveraging

    Financing Cash Flow negative

    AND

    Borrowings declining
    """

    if financing_activity >= 0:
        return False

    if previous_borrowings is None:
        return False

    if current_borrowings is None:
        return False

    return current_borrowings < previous_borrowings

# ==========================================================
# Cash Flow Intelligence
# ==========================================================

def generate_cashflow_summary(
        cfo_quality,
        capex_label,
        distress,
        deleveraging):
    """
    Overall label
    """

    if distress:
        return "Distress"

    if deleveraging:
        return "Deleveraging"

    if (
        cfo_quality == "High Quality"
        and capex_label == "Asset Light"
    ):
        return "Efficient Compounder"

    if (
        cfo_quality == "High Quality"
        and capex_label == "Capital Intensive"
    ):
        return "Capital Intensive Compounder"

    if cfo_quality == "Moderate":
        return "Stable"

    return "Needs Monitoring"

# ==========================================================
# Distress Signal Detection
# ==========================================================

def detect_distress_signal(
        operating_activity,
        financing_activity):
    """
    Distress Signal

    CFO < 0
    AND
    Financing Cash Flow > 0
    """

    operating_activity = operating_activity or 0
    financing_activity = financing_activity or 0

    return (
        operating_activity < 0
        and financing_activity > 0
    )


# ==========================================================
# DAY 31
# CASH FLOW INTELLIGENCE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 31")
    print("Cash Flow Intelligence")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    """
    SELECT *
    FROM cashflow
    ORDER BY company_id, year
    """,
    conn
)

profit = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        operating_profit
    FROM profitandloss
    ORDER BY company_id, year
    """,
    conn
)

companies = pd.read_sql(
    """
    SELECT
        id,
        company_name
    FROM companies
    """,
    conn
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn
)

print()

print("Cashflow Records :", len(cashflow))
print("Profit Records   :", len(profit))
print("Companies        :", len(companies))
print("Sectors          :", len(sectors))

print()
print(cashflow.head())


# ==========================================================
# LOAD CAPITAL ALLOCATION
# ==========================================================

CAPITAL_FILE = OUTPUT_DIR / "capital_allocation.csv"

print()
print("=" * 60)
print("DAY 32")
print("Capital Allocation Report")
print("=" * 60)

if CAPITAL_FILE.exists():

    capital = pd.read_csv(CAPITAL_FILE)

else:

    raise FileNotFoundError(
        f"{CAPITAL_FILE} not found."
    )

# ==========================================================
# KEEP ONLY MASTER COMPANIES
# ==========================================================

capital = capital[
    capital["company_id"].isin(companies["id"])
].copy()

print()

print("Capital Allocation Records :", len(capital))

print("Unique Companies :", capital["company_id"].nunique())

print("Unique Years :", capital["year"].nunique())

print()

print(capital.head())


# ==========================================================
# VALIDATE CAPITAL ALLOCATION
# ==========================================================

print()

print("=" * 60)
print("VALIDATING CAPITAL ALLOCATION")
print("=" * 60)

expected = companies["id"].nunique()

actual = capital["company_id"].nunique()

print("Expected Companies :", expected)
print("Available Companies :", actual)

missing = sorted(
    set(companies["id"]) -
    set(capital["company_id"])
)

if len(missing):

    print()

    print("Missing Companies")

    print(missing)

else:

    print()

    print("All companies available.")


# ==========================================================
# LATEST YEAR DISTRIBUTION
# ==========================================================

print()

print("=" * 60)
print("LATEST YEAR DISTRIBUTION")
print("=" * 60)

# ==========================================================
# LATEST RECORD OF EACH COMPANY
# ==========================================================

capital = capital.sort_values(
    ["company_id", "year"]
)

latest = (
    capital
    .groupby("company_id", as_index=False)
    .tail(1)
)

print("Companies in Latest Snapshot :", len(latest))

distribution = (
    latest
    .groupby("pattern_label")
    .size()
    .reset_index(name="company_count")
    .sort_values("company_count", ascending=False)
)

print()
print(distribution)

# ==========================================================
# PROCESS ALL COMPANIES
# ==========================================================

results = []

distress_alerts = []

company_ids = sorted(companies["id"].unique())

print("=" * 60)
print("COMPANY VALIDATION")
print("=" * 60)

print("Companies in Master Table :", len(companies["id"].unique()))
print("Companies to Process      :", len(company_ids))

print()
print("=" * 60)
print("Calculating Cash Flow Intelligence")
print("=" * 60)

master_companies = set(companies["id"])
cashflow_companies = set(cashflow["company_id"])
profit_companies = set(profit["company_id"])

print("=" * 60)
print("MISSING COMPANY CHECK")
print("=" * 60)

print("Missing in Cashflow:")
print(sorted(master_companies - cashflow_companies))

print()

print("Missing in Profit:")
print(sorted(master_companies - profit_companies))


# ==========================================================
# PROCESS ALL COMPANIES
# ==========================================================

results = []
distress_alerts = []

company_ids = sorted(companies["id"].unique())

print()
print("=" * 60)
print("Calculating Cash Flow Intelligence")
print("=" * 60)

for company_id in company_ids:

    # ------------------------------------------------------
    # Cash Flow Data
    # ------------------------------------------------------

    cf = (
        cashflow[cashflow["company_id"] == company_id]
        .sort_values("year")
        .tail(5)
        .copy()
    )

    # ------------------------------------------------------
    # Company Name
    # ------------------------------------------------------

    company_name = companies.loc[
        companies["id"] == company_id,
        "company_name"
    ]

    if len(company_name):
        company_name = company_name.iloc[0]
    else:
        company_name = company_id

    # ------------------------------------------------------
    # Sector
    # ------------------------------------------------------

    sector = sectors.loc[
        sectors["company_id"] == company_id,
        "broad_sector"
    ]

    if len(sector):
        sector = sector.iloc[0]
    else:
        sector = "Unknown"

    # ------------------------------------------------------
    # No Cashflow Data
    # ------------------------------------------------------

    if cf.empty:

        results.append({

            "company_id": company_id,
            "company_name": company_name,
            "sector": sector,

            "cfo_quality_score": None,
            "cfo_quality_label": "NO_DATA",

            "capex_intensity_pct": None,
            "capex_label": "NO_DATA",

            "fcf_cagr_5yr": None,
            "fcf_conversion_pct": None,

            "distress_flag": False,
            "deleveraging_flag": False,

            "capital_allocation_label": "NO_DATA",

            "summary": "Cash flow data unavailable."

        })

        continue

    # ------------------------------------------------------
    # Profit Data
    # ------------------------------------------------------

    pl = (
        profit[profit["company_id"] == company_id]
        .sort_values("year")
        .tail(5)
        .copy()
    )

    if pl.empty:

        results.append({

            "company_id": company_id,
            "company_name": company_name,
            "sector": sector,

            "cfo_quality_score": None,
            "cfo_quality_label": "NO_DATA",

            "capex_intensity_pct": None,
            "capex_label": "NO_DATA",

            "fcf_cagr_5yr": None,
            "fcf_conversion_pct": None,

            "distress_flag": False,
            "deleveraging_flag": False,

            "capital_allocation_label": "NO_DATA",

            "summary": "Profit data unavailable."

        })

        continue

    # ------------------------------------------------------
    # Latest Records
    # ------------------------------------------------------

    latest_cf = cf.iloc[-1]
    latest_pl = pl.iloc[-1]

    # ------------------------------------------------------
    # Lists
    # ------------------------------------------------------

    cfo_values = (
        cf["operating_activity"]
        .fillna(0)
        .tolist()
    )

    investing_values = (
        cf["investing_activity"]
        .fillna(0)
        .tolist()
    )

    financing_values = (
        cf["financing_activity"]
        .fillna(0)
        .tolist()
    )

    pat_values = (
        pl["net_profit"]
        .fillna(0)
        .tolist()
    )

    sales_values = (
        pl["sales"]
        .fillna(0)
        .tolist()
    )

    operating_profit_values = (
        pl["operating_profit"]
        .fillna(0)
        .tolist()
    )

    # ------------------------------------------------------
    # Free Cash Flow
    # ------------------------------------------------------

    fcf_values = []

    for cfo, inv in zip(cfo_values, investing_values):

        fcf = calculate_free_cash_flow(
            cfo,
            inv
        )

        fcf_values.append(fcf)

    # ------------------------------------------------------
    # KPI Calculations
    # ------------------------------------------------------

    cfo_score, cfo_label = calculate_cfo_quality_score(
        cfo_values,
        pat_values
    )

    capex_pct, capex_label = calculate_capex_intensity(
        latest_cf["investing_activity"],
        latest_pl["sales"]
    )

    fcf_cagr = calculate_fcf_cagr(
        fcf_values
    )

    latest_fcf = fcf_values[-1]

    fcf_conversion = calculate_fcf_conversion_rate(
        latest_fcf,
        latest_pl["operating_profit"]
    )

    distress = detect_distress_signal(
        latest_cf["operating_activity"],
        latest_cf["financing_activity"]
    )

    previous_borrowings = 0
    current_borrowings = 0

    if "borrowings" in cf.columns and len(cf) >= 2:

        previous_borrowings = cf.iloc[-2]["borrowings"]
        current_borrowings = cf.iloc[-1]["borrowings"]

    deleveraging = detect_deleveraging(
        latest_cf["financing_activity"],
        previous_borrowings,
        current_borrowings
    )

    allocation = classify_capital_allocation(
        latest_cf["operating_activity"],
        latest_cf["investing_activity"],
        latest_cf["financing_activity"],
        cfo_score
    )

    summary = generate_cashflow_summary(
        cfo_label,
        capex_label,
        distress,
        deleveraging
    )

    # ------------------------------------------------------
    # Save Result
    # ------------------------------------------------------

    results.append({

        "company_id": company_id,
        "company_name": company_name,
        "sector": sector,
        "cfo_quality_score": cfo_score,
        "cfo_quality_label": cfo_label,
        "capex_intensity_pct": capex_pct,
        "capex_label": capex_label,
        "fcf_cagr_5yr": fcf_cagr,
        "fcf_conversion_pct": fcf_conversion,
        "distress_flag": distress,
        "deleveraging_flag": deleveraging,
        "capital_allocation_label": allocation,
        "summary": summary

    })

    if distress:

        distress_alerts.append({

            "company_id": company_id,
            "company_name": company_name,
            "CFO": latest_cf["operating_activity"],
            "CFF": latest_cf["financing_activity"],
            "Latest Net Profit": latest_pl["net_profit"]

        })

print()
print("Companies Processed :", len(results))
print("Distress Alerts     :", len(distress_alerts))


# ==========================================================
# CREATE DATAFRAMES
# ==========================================================

results_df = pd.DataFrame(results)

# ==========================================================
# MERGE CAPITAL ALLOCATION
# ==========================================================

latest_allocation = (

    latest[
        [
            "company_id",
            "pattern_label"
        ]
    ]

)

results_df = results_df.merge(
    latest_allocation,
    on="company_id",
    how="left"
)

results_df.rename(
    columns={
        "pattern_label":
        "capital_allocation"
    },
    inplace=True
)

print()

print("Capital Allocation merged into results.")


distress_df = pd.DataFrame(distress_alerts)

# ==========================================================
# PATTERN CHANGE REPORT
# ==========================================================

print()

print("=" * 60)
print("PATTERN CHANGES")
print("=" * 60)

changes = []

for company in capital["company_id"].unique():

    history = (

        capital[
            capital["company_id"] == company
        ]

        .sort_values("year")

    )

    if len(history) < 2:
        continue

    previous = history.iloc[-2]

    current = history.iloc[-1]

    if (

        previous["pattern_label"]

        !=

        current["pattern_label"]

    ):

        company_row = companies.loc[
            companies["id"] == company,
            "company_name"
        ]

        if company_row.empty:
             company_name = company
        else:
            company_name = company_row.iloc[0]



        changes.append({

            "company_id": company,

            "company_name": company_name,

            "previous_year": previous["year"],

            "previous_pattern":
            previous["pattern_label"],

            "current_year":
            current["year"],

            "current_pattern":
            current["pattern_label"],

        })

changes_df = pd.DataFrame(changes)

print()

print("Pattern Changes :", len(changes_df))

print()
print("=" * 60)
print("CHECKING FOR DUPLICATES")
print("=" * 60)

print("Total Rows :", len(results_df))
print("Unique Companies :", results_df["company_id"].nunique())

duplicates = results_df[
    results_df.duplicated(subset="company_id", keep=False)
]

if duplicates.empty:
    print("No duplicate companies found.")
else:
    print("Duplicate Companies Found:")
    print(duplicates[["company_id"]].drop_duplicates())

print()
print("=" * 60)
print("Creating Output Files")
print("=" * 60)

results_df = results_df.sort_values("company_id")
distress_df = distress_df.sort_values("company_id")

excel_file = OUTPUT_DIR / "cashflow_intelligence.xlsx"
csv_file = OUTPUT_DIR / "distress_alerts.csv"

results_df.to_excel(
    excel_file,
    index=False
)

# ==========================================================
# SAVE PATTERN CHANGES
# ==========================================================

pattern_file = OUTPUT_DIR / "pattern_changes.csv"

changes_df.to_csv(

    pattern_file,

    index=False

)

print()

print("Pattern Change Report Saved")

print(pattern_file)


distress_df.to_csv(
    csv_file,
    index=False
)

print()
print("Cash Flow Records :", len(results_df))
print("Distress Records  :", len(distress_df))

print()
print("Excel Saved")
print(excel_file)

print()
print("CSV Saved")
print(csv_file)

conn.close()

print()
print("=" * 60)
print("DAY 32 COMPLETED")
print("Capital Allocation Report Generated Successfully")
print("=" * 60)

# ==========================================================
# VALIDATION
# ==========================================================

print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)

required_columns = [
    "company_id",
    "company_name",
    "sector",
    "cfo_quality_score",
    "cfo_quality_label",
    "capex_intensity_pct",
    "capex_label",
    "fcf_cagr_5yr",
    "fcf_conversion_pct",
    "distress_flag",
    "deleveraging_flag",
    "capital_allocation_label"
]

missing_columns = [
    col for col in required_columns
    if col not in results_df.columns
]

if not missing_columns:
    print("✓ All required columns present")
else:
    print("Missing Columns:")
    print(missing_columns)

print()
print("Companies Processed :", len(results_df))
print("Distress Alerts     :", len(distress_df))

print()
print("CFO Quality Distribution")
print(results_df["cfo_quality_label"].value_counts(dropna=False))

print()
print("CapEx Distribution")
print(results_df["capex_label"].value_counts(dropna=False))

print()
print("Capital Allocation Distribution")
print(results_df["capital_allocation_label"].value_counts(dropna=False))

print()
print("Files Generated")
print(excel_file)
print(csv_file)

conn.close()

print()

print("=" * 60)
print("DAY 31 & DAY 32 COMPLETED")
print("=" * 60)