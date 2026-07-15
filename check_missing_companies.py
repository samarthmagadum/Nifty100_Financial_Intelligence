from src.etl.loader import load_core_files

core = load_core_files()

missing = [
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE"
]

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons"
]

print("=" * 80)
print("CHECKING WHICH TABLES CONTAIN THE MISSING COMPANIES")
print("=" * 80)

for company in missing:

    print("\n" + "=" * 60)
    print(company)
    print("=" * 60)

    found = False

    for table in tables:

        df = core[table]

        if "company_id" not in df.columns:
            continue

        rows = df[df["company_id"] == company]

        if len(rows) > 0:
            found = True
            print(f"\nFound in {table} : {len(rows)} rows")

            print(rows.head())

    if not found:
        print("Not present in any core dataset.")