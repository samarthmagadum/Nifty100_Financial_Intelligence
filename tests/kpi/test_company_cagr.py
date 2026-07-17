from src.etl.loader import load_core_files
from src.analytics.ratio_engine import calculate_company_cagr

print("=" * 60)
print("Loading Data")
print("=" * 60)

core_data = load_core_files()

profitandloss = core_data["profitandloss"]

print("\nCalculating CAGR...")

result = calculate_company_cagr(profitandloss)

print("\nFirst 10 Companies")

print(result.head(10))

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("Total Companies:", len(result))