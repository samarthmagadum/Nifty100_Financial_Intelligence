"""
Sprint 2 - Day 13

Compare calculated ratios with source values
and generate ratio_edge_cases.log
"""

import pandas as pd
from pathlib import Path

from src.etl.loader import (
    load_core_files,
    load_supporting_files
)

def load_data():

    print("=" * 60)
    print("LOADING DATA")
    print("=" * 60)

    core = load_core_files()
    supporting = load_supporting_files()

    companies = core["companies"]
    financial_ratios = supporting["financial_ratios"]
    sectors = supporting["sectors"]

    return companies, financial_ratios, sectors


def prepare_data():

    companies, financial_ratios, sectors = load_data()

    # Merge company master
    df = financial_ratios.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )

    # Merge sector information
    df = df.merge(
        sectors[["company_id", "broad_sector"]],
        on="company_id",
        how="left"
    )

    print("\nMerged Rows :", len(df))

    return df

OUTPUT_FOLDER = Path("output")

OUTPUT_FOLDER.mkdir(exist_ok=True)

LOG_FILE = OUTPUT_FOLDER / "ratio_edge_cases.log"


def generate_log(df):

    print("\nGenerating Edge Case Log...")

    total = 0

    with open(LOG_FILE, "w", encoding="utf-8") as file:

        file.write("RATIO EDGE CASES\n")
        file.write("=" * 80 + "\n\n")

        for _, row in df.iterrows():

            # -----------------------------
            # Financial Sector Carve-Out
            # -----------------------------
            sector = row.get("broad_sector")

            if sector == "Financials":
             continue

            calc_roe = row.get("return_on_equity_pct")
            source_roe = row.get("roe_percentage")

            if (
                pd.notna(calc_roe)
                and pd.notna(source_roe)
                and abs(calc_roe - source_roe) > 5
            ):

                difference = abs(calc_roe - source_roe)

                if difference > 20:
                    category = "Data Source Issue"
                elif difference > 10:
                    category = "Version Difference"
                else:
                    category = "Formula Difference"

                file.write(
                     f"{row['company_id']} | "
                     f"{row['year']} | "
                     f"{category} | "
                     f"Calculated={calc_roe:.2f} | "
                     f"Source={source_roe:.2f}\n"
                 ) 

                total += 1

        file.write("\n")
        file.write("=" * 80 + "\n")
        file.write(f"Total Anomalies : {total}\n")

    print(f"Log Created : {LOG_FILE}")
    print(f"Total Anomalies : {total}")

if __name__ == "__main__":

    df = prepare_data()

    generate_log(df)