"""
cashflow_kpis.py

Sprint 2 - Day 11
Cash Flow KPI Functions
"""

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