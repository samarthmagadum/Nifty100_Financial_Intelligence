"""
ratios.py

Purpose
-------
Contains all financial ratio calculation functions.

Project : Nifty100 Financial Intelligence Platform
"""

# ==========================================================
# Net Profit Margin
# ==========================================================

def calculate_net_profit_margin(net_profit, sales):
    """
    Calculate Net Profit Margin.

    Formula
    -------
    (Net Profit / Sales) * 100

    Parameters
    ----------
    net_profit : float

    sales : float

    Returns
    -------
    float or None
    """

    # Handle missing or zero sales
    if sales is None or sales == 0:
        return None

    # Calculate Net Profit Margin
    margin = (net_profit / sales) * 100

    # Round to 2 decimal places
    return round(margin, 2)


# ==========================================================
# Operating Profit Margin
# ==========================================================

def calculate_operating_profit_margin(
        operating_profit,
        sales,
        opm_percentage=None):
    """
    Calculate Operating Profit Margin.

    Formula
    -------
    (Operating Profit / Sales) * 100

    Parameters
    ----------
    operating_profit : float

    sales : float

    opm_percentage : float
        Existing value from dataset (optional)

    Returns
    -------
    float or None
    """

    # Handle zero or missing sales
    if sales is None or sales == 0:
        return None

    # Calculate OPM
    calculated_opm = (operating_profit / sales) * 100

    calculated_opm = round(calculated_opm, 2)

    # Cross-check with dataset value
    if opm_percentage is not None:

        difference = abs(calculated_opm - opm_percentage)

        if difference > 1:

            print("=" * 60)
            print("⚠ OPM MISMATCH")
            print("=" * 60)
            print(f"Calculated : {calculated_opm}")
            print(f"Dataset    : {opm_percentage}")
            print(f"Difference : {difference:.2f}%")

    return calculated_opm


# ==========================================================
# Return on Equity (ROE)
# ==========================================================

def calculate_roe(
        net_profit,
        equity_capital,
        reserves):
    """
    Calculate Return on Equity (ROE).

    Formula
    -------
    (Net Profit / (Equity Capital + Reserves)) * 100

    Parameters
    ----------
    net_profit : float

    equity_capital : float

    reserves : float

    Returns
    -------
    float or None
    """

    # Handle None values
    equity_capital = equity_capital or 0
    reserves = reserves or 0

    total_equity = equity_capital + reserves

    # Edge Case
    if total_equity <= 0:
        return None

    roe = (net_profit / total_equity) * 100

    return round(roe, 2)


# ==========================================================
# Return on Capital Employed (ROCE)
# ==========================================================

def calculate_roce(
        operating_profit,
        other_income,
        interest,
        equity_capital,
        reserves,
        borrowings):
    """
    Calculate Return on Capital Employed (ROCE).

    Formula
    -------
    EBIT = Operating Profit + Other Income - Interest

    ROCE = EBIT / (Equity + Reserves + Borrowings) * 100
    """

    # Replace None with 0
    operating_profit = operating_profit or 0
    other_income = other_income or 0
    interest = interest or 0
    equity_capital = equity_capital or 0
    reserves = reserves or 0
    borrowings = borrowings or 0

    # Calculate EBIT
    ebit = operating_profit + other_income - interest

    # Calculate Capital Employed
    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    # Edge Case
    if capital_employed <= 0:
        return None

    roce = (ebit / capital_employed) * 100

    return round(roce, 2)


# ==========================================================
# Return on Assets (ROA)
# ==========================================================

def calculate_roa(
        net_profit,
        total_assets):
    """
    Calculate Return on Assets (ROA).

    Formula
    -------
    (Net Profit / Total Assets) * 100

    Parameters
    ----------
    net_profit : float

    total_assets : float

    Returns
    -------
    float or None
    """

    # Handle None
    total_assets = total_assets or 0

    # Edge Case
    if total_assets <= 0:
        return None

    roa = (net_profit / total_assets) * 100

    return round(roa, 2)


# ==========================================================
# Debt-to-Equity Ratio
# ==========================================================

def calculate_debt_to_equity(
        borrowings,
        equity_capital,
        reserves):
    """
    Calculate Debt-to-Equity Ratio.

    Formula
    -------
    Borrowings / (Equity Capital + Reserves)

    Returns
    -------
    float
    """

    borrowings = borrowings or 0
    equity_capital = equity_capital or 0
    reserves = reserves or 0

    # Debt-free company
    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    # Invalid denominator
    if total_equity <= 0:
        return None

    ratio = borrowings / total_equity

    return round(ratio, 2)

# ==========================================================
# High Leverage Flag
# ==========================================================

def high_leverage_flag(
        debt_to_equity,
        broad_sector):
    """
    Returns True if company has high leverage.

    Financial sector companies are ignored.
    """

    if debt_to_equity is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_to_equity > 5


# ==========================================================
# Interest Coverage Ratio (ICR)
# ==========================================================

def calculate_interest_coverage(
        operating_profit,
        other_income,
        interest):
    """
    Calculate Interest Coverage Ratio.

    Formula
    -------
    (Operating Profit + Other Income) / Interest
    """

    operating_profit = operating_profit or 0
    other_income = other_income or 0
    interest = interest or 0

    # Debt-free company
    if interest == 0:
        return None

    icr = (operating_profit + other_income) / interest

    return round(icr, 2)


# ==========================================================
# ICR Label
# ==========================================================

def get_icr_label(interest):
    """
    Returns Debt Free if interest is zero.
    """

    interest = interest or 0

    if interest == 0:
        return "Debt Free"

    return "Normal"


# ==========================================================
# ICR Warning Flag
# ==========================================================

def icr_warning_flag(icr):
    """
    Returns True if ICR is less than 1.5
    """

    if icr is None:
        return False

    return icr < 1.5


# ==========================================================
# Net Debt
# ==========================================================

def calculate_net_debt(
        borrowings,
        investments):
    """
    Calculate Net Debt.

    Formula
    -------
    Borrowings - Investments
    """

    borrowings = borrowings or 0
    investments = investments or 0

    net_debt = borrowings - investments

    return round(net_debt, 2)


# ==========================================================
# Asset Turnover Ratio
# ==========================================================

def calculate_asset_turnover(
        sales,
        total_assets):
    """
    Calculate Asset Turnover Ratio.

    Formula
    -------
    Sales / Total Assets
    """

    sales = sales or 0
    total_assets = total_assets or 0

    if total_assets <= 0:
        return None

    turnover = sales / total_assets

    return round(turnover, 2)