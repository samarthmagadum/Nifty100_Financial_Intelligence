"""
normaliser.py

This file contains functions to clean and standardize data.


"""

import pandas as pd


# --------------------------------------------------
# Normalize Company ID / Ticker
# --------------------------------------------------
def normalize_ticker(value):
    """
    Convert ticker/company ID into a standard format.

    Example:
    " tcs " -> "TCS"
    "infy"  -> "INFY"
    """

    # Return None if value is empty
    if pd.isna(value):
        return None

    # Convert to string
    value = str(value)

    # Remove extra spaces
    value = value.strip()

    # Convert to uppercase
    value = value.upper()

    return value


# --------------------------------------------------
# Normalize Year
# --------------------------------------------------
def normalize_year(value):
    """
    Convert year labels into a common format.

    Example:
    Mar-23 -> 2023-03
    Dec-24 -> 2024-12
    """

    # Return None if empty
    if pd.isna(value):
        return None

    # Convert to string
    value = str(value).strip()

    # Dictionary containing year conversions
    year_mapping = {

        # March Financial Year
        "Mar-20": "2020-03",
        "Mar-21": "2021-03",
        "Mar-22": "2022-03",
        "Mar-23": "2023-03",
        "Mar-24": "2024-03",
        "Mar-25": "2025-03",

        # December Financial Year
        "Dec-20": "2020-12",
        "Dec-21": "2021-12",
        "Dec-22": "2022-12",
        "Dec-23": "2023-12",
        "Dec-24": "2024-12",

    }

    # Return converted value if found
    if value in year_mapping:
        return year_mapping[value]

    # Otherwise return original value
    return value