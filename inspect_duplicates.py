from src.etl.loader import load_core_files

data = load_core_files()

balance = data["balancesheet"]
cashflow = data["cashflow"]

print("=" * 70)
print("BALANCE SHEET DUPLICATES")
print("=" * 70)

print(
    balance[
        (balance["company_id"] == "ASIANPAINT") &
        (balance["year"] == "Mar 2013")
    ]
)

print("\n")

print("=" * 70)
print("CASHFLOW DUPLICATES")
print("=" * 70)

print(
    cashflow[
        (cashflow["company_id"] == "ABB") &
        (cashflow["year"] == "Mar 2014")
    ]
)