import pandas as pd
import numpy as np

def winsorize(series):
    """
    Caps values between 10th and 90th percentile.
    """

    lower = series.quantile(0.10)
    upper = series.quantile(0.90)

    return series.clip(lower, upper)

def normalize(series):
    """
    Convert values to 0–100 scale.
    """

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(50, index=series.index)

    return (
        (series - minimum)
        / (maximum - minimum)
    ) * 100

def normalize_inverse(series):
    """
    Lower values receive higher scores.
    """

    return 100 - normalize(series)

def calculate_composite_score(df):

    print()
    print("=" * 60)
    print("CALCULATING COMPOSITE SCORE")
    print("=" * 60)

    score_df = df.copy()


    # ---------------------------------
    # Profitability Metrics
    # ---------------------------------

    score_df["roe_score"] = normalize(
        winsorize(score_df["return_on_equity_pct"])
    )

    score_df["npm_score"] = normalize(
        winsorize(score_df["net_profit_margin_pct"])
    )