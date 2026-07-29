"""
ratio_engine_db.py

Sprint 2 - Day 12

Populate financial_ratios table in SQLite.
"""

import pandas as pd

from src.etl.loader import load_core_files
from src.database.database_utils import get_connection

from src.analytics.ratio_engine import (
    calculate_company_cagr
)

from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    calculate_roe,
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_asset_turnover
)

from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_capex_intensity
)

from src.analytics.cagr import (
    calculate_cagr
)





def load_data():

    print("=" * 60)
    print("LOADING DATA")
    print("=" * 60)

    data = load_core_files()

    profit = data["profitandloss"]

    balance = data["balancesheet"]

    cashflow = data["cashflow"]

    return profit, balance, cashflow



def prepare_dataset():

    # Load data
    profit, balance, cashflow = load_data()

    # ------------------------------------------------------
    # Clean Balance Sheet
    # ------------------------------------------------------
    balance = (
        balance
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
    )

    # ------------------------------------------------------
    # Clean Cash Flow
    # ------------------------------------------------------
    cashflow = (
        cashflow
        .sort_values(
            by="operating_activity",
            ascending=False
        )
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
    )

    # ------------------------------------------------------
    # Print Row Counts
    # ------------------------------------------------------
    print("\nAfter Cleaning")

    print("Profit & Loss :", len(profit))
    print("Balance Sheet :", len(balance))
    print("Cash Flow     :", len(cashflow))

    # ------------------------------------------------------
    # Merge DataFrames
    # ------------------------------------------------------
    df = profit.merge(
        balance,
        on=["company_id", "year"],
        how="inner"
    )

    df = df.merge(
        cashflow,
        on=["company_id", "year"],
        how="inner"
    )

    print("\nMerged Rows :", len(df))
    print(df.head())

    return df


def calculate_kpis(df):

    print("\n" + "=" * 60)
    print("CALCULATING KPIs")
    print("=" * 60)

    print("\nCalculating CAGR...")

    # Calculate CAGR for each company
    cagr_df = calculate_company_cagr(df)

    # Merge CAGR values into every yearly record
    df = df.merge(
        cagr_df[
            [
                "company_id",
                "revenue_cagr_5yr",
                "pat_cagr_5yr",
                "eps_cagr_5yr"
            ]
        ],
        on="company_id",
        how="left"
    )

    results = []

    for _, row in df.iterrows():

        net_profit_margin = calculate_net_profit_margin(
            row["net_profit"],
            row["sales"]
        )

        operating_profit_margin = calculate_operating_profit_margin(
            row["operating_profit"],
            row["sales"]
        )

        roe = calculate_roe(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"]
        )

        debt_to_equity = calculate_debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        )

        interest_coverage = calculate_interest_coverage(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        )

        asset_turnover = calculate_asset_turnover(
            row["sales"],
            row["total_assets"]
        )

        free_cash_flow = calculate_free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        )

        capex_value, capex_label = calculate_capex_intensity(
            row["investing_activity"],
            row["sales"]
        )

        if row["equity_capital"] > 0:
            book_value = (
                row["equity_capital"] + row["reserves"]
            ) / row["equity_capital"]
        else:
            book_value = None

        results.append({

            "company_id": row["company_id"],
            "year": row["year"],

            "net_profit_margin_pct": net_profit_margin,
            "operating_profit_margin_pct": operating_profit_margin,
            "return_on_equity_pct": roe,
            "debt_to_equity": debt_to_equity,
            "interest_coverage": interest_coverage,
            "asset_turnover": asset_turnover,
            "free_cash_flow_cr": free_cash_flow,
            "capex_cr": capex_value,

            "earnings_per_share": row["eps"],
            "book_value_per_share": book_value,

            "dividend_payout_ratio_pct": row["dividend_payout"],
            "total_debt_cr": row["borrowings"],
            "cash_from_operations_cr": row["operating_activity"],

            "revenue_cagr_5yr": row["revenue_cagr_5yr"],
            "pat_cagr_5yr": row["pat_cagr_5yr"],
            "eps_cagr_5yr": row["eps_cagr_5yr"],

            "composite_quality_score": None

        })

    result = pd.DataFrame(results)

    print("\nKPI Rows :", len(result))
    print(result.head())

    return result

def update_financial_ratios(df):

    print("\n" + "=" * 60)
    print("UPDATING SQLITE DATABASE")
    print("=" * 60)

    connection = get_connection()

    cursor = connection.cursor()

    updated = 0

    for _, row in df.iterrows():

        cursor.execute("""
        UPDATE financial_ratios

        SET
            net_profit_margin_pct=?,
            operating_profit_margin_pct=?,
            return_on_equity_pct=?,
            debt_to_equity=?,
            interest_coverage=?,
            asset_turnover=?,
            free_cash_flow_cr=?,
            capex_cr=?,
            earnings_per_share=?,
            book_value_per_share=?,
            dividend_payout_ratio_pct=?,
            total_debt_cr=?,
            cash_from_operations_cr=?,
            revenue_cagr_5yr=?,
            pat_cagr_5yr=?,
            eps_cagr_5yr=?,
            composite_quality_score=?

        WHERE
            company_id=?
            AND year=?
        """,

        (

            row["net_profit_margin_pct"],
            row["operating_profit_margin_pct"],
            row["return_on_equity_pct"],
            row["debt_to_equity"],
            row["interest_coverage"],
            row["asset_turnover"],
            row["free_cash_flow_cr"],
            row["capex_cr"],
            row["earnings_per_share"],
            row["book_value_per_share"],
            row["dividend_payout_ratio_pct"],
            row["total_debt_cr"],
            row["cash_from_operations_cr"],
            row["revenue_cagr_5yr"],
            row["pat_cagr_5yr"],
            row["eps_cagr_5yr"],
            row["composite_quality_score"],

            row["company_id"],
            row["year"]

        ))

        updated += cursor.rowcount

    connection.commit()

    connection.close()

    print(f"\nUpdated Rows : {updated}")


if __name__ == "__main__":

    merged = prepare_dataset()

    kpis = calculate_kpis(merged)

    update_financial_ratios(kpis)

 