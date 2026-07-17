import pandas as pd

from src.analytics.cagr import calculate_cagr

# ==========================================================
# Get CAGR for any metric
# ==========================================================

def get_cagr(df, column, years):
    """
    Calculate CAGR for a given column over the specified number of years.

    Parameters
    ----------
    df : Company data sorted by year
    column : sales / net_profit / eps
    years : 3, 5, or 10

    Returns
    -------
    (value, flag)
    """

    # Need at least years + 1 records
    if len(df) < years + 1:
        return None, "INSUFFICIENT"

    start_value = df.iloc[-(years + 1)][column]
    end_value = df.iloc[-1][column]

    return calculate_cagr(
        start_value,
        end_value,
        years
    )


# ==========================================================
# Calculate CAGR for All Companies
# ==========================================================

def calculate_company_cagr(profitandloss_df):
    """
    Calculate Revenue, PAT and EPS CAGR
    for every company.

    Returns
    -------
    DataFrame
    """

    results = []

    # Process one company at a time
    for company_id, group in profitandloss_df.groupby("company_id"):

        # Remove TTM rows
        group = group[group["year"] != "TTM"]

        # Reset index
        group = group.reset_index(drop=True)

        # Skip if no data
        if len(group) == 0:
            continue

        revenue_3, revenue_3_flag = get_cagr(group, "sales", 3)
        revenue_5, revenue_5_flag = get_cagr(group, "sales", 5)
        revenue_10, revenue_10_flag = get_cagr(group, "sales", 10)

        pat_3, pat_3_flag = get_cagr(group, "net_profit", 3)
        pat_5, pat_5_flag = get_cagr(group, "net_profit", 5)
        pat_10, pat_10_flag = get_cagr(group, "net_profit", 10)

        eps_3, eps_3_flag = get_cagr(group, "eps", 3)
        eps_5, eps_5_flag = get_cagr(group, "eps", 5)
        eps_10, eps_10_flag = get_cagr(group, "eps", 10)

        results.append({

            "company_id": company_id,

            "revenue_cagr_3yr": revenue_3,
            "revenue_cagr_3yr_flag": revenue_3_flag,

            "revenue_cagr_5yr": revenue_5,
            "revenue_cagr_5yr_flag": revenue_5_flag,

            "revenue_cagr_10yr": revenue_10,
            "revenue_cagr_10yr_flag": revenue_10_flag,

            "pat_cagr_3yr": pat_3,
            "pat_cagr_3yr_flag": pat_3_flag,

            "pat_cagr_5yr": pat_5,
            "pat_cagr_5yr_flag": pat_5_flag,

            "pat_cagr_10yr": pat_10,
            "pat_cagr_10yr_flag": pat_10_flag,

            "eps_cagr_3yr": eps_3,
            "eps_cagr_3yr_flag": eps_3_flag,

            "eps_cagr_5yr": eps_5,
            "eps_cagr_5yr_flag": eps_5_flag,

            "eps_cagr_10yr": eps_10,
            "eps_cagr_10yr_flag": eps_10_flag

        })

    return pd.DataFrame(results)