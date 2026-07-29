import pandas as pd


def clean_dataframe(df):

    df = df.copy()


    df = df.replace(
        [
            None,
            "None",
            "nan",
            "NaN",
            ""
        ],
        pd.NA
    )


    return df



def safe_value(value):

    if pd.isna(value):

        return "N/A"

    return value