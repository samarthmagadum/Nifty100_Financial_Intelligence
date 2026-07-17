import pandas as pd
from pathlib import Path

from src.analytics.cashflow_kpis import classify_capital_allocation
from src.etl.loader import load_core_files


def generate_capital_allocation():

    print("=" * 60)
    print("GENERATING CAPITAL ALLOCATION")
    print("=" * 60)

    core_data = load_core_files()

    cashflow = core_data["cashflow"]

    rows = []

    for _, row in cashflow.iterrows():

        pattern = classify_capital_allocation(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"]
        )

        rows.append({
            "company_id": row["company_id"],
            "year": row["year"],
            "cfo_sign": "+" if row["operating_activity"] >= 0 else "-",
            "cfi_sign": "+" if row["investing_activity"] >= 0 else "-",
            "cff_sign": "+" if row["financing_activity"] >= 0 else "-",
            "pattern_label": pattern
        })

    result = pd.DataFrame(rows)

    # Create output folder if it doesn't exist
    Path("output").mkdir(exist_ok=True)

    output_file = Path("output") / "capital_allocation.csv"

    result.to_csv(output_file, index=False)

    print(f"\nRows Generated : {len(result)}")
    print(f"Saved To       : {output_file.resolve()}")

    print("\nFirst 10 Rows")
    print(result.head(10))

    print("\n✅ capital_allocation.csv generated successfully")


if __name__ == "__main__":
    generate_capital_allocation()