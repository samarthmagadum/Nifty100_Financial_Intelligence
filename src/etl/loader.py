"""
loader.py

Purpose:
--------
This file loads all Excel datasets into pandas DataFrames.


"""

# ----------------------------------------------------------
# Import Required Libraries
# ----------------------------------------------------------

import pandas as pd

# Import project configuration
from src.etl.config import (
    RAW_DATA_DIR,
    SUPPORTING_DATA_DIR,
    CORE_FILES,
    SUPPORTING_FILES
)
# ----------------------------------------------------------
# Function to Load One Excel File
# ----------------------------------------------------------

def load_excel(file_path, header_row=0):
    """
    Reads an Excel file and returns a DataFrame.

    Parameters
    ----------
    file_path : Path
        Excel file path

    header_row : int
        Row number containing column names
    """

    try:

        # Read Excel File
        df = pd.read_excel(file_path, header=header_row)

        print(f"✅ Loaded : {file_path.name}")

        return df

    except Exception as e:

        print(f"❌ Error loading : {file_path.name}")
        print(e)

        return None


# ----------------------------------------------------------
# Load Core Files
# Core datasets use header row = 1
# ----------------------------------------------------------

def load_core_files():

    core_data = {}

    print("\nLoading Core Files...\n")

    for dataset_name, file_name in CORE_FILES.items():

        file_path = RAW_DATA_DIR / file_name

        # Core datasets have headers on second row
        core_data[dataset_name] = load_excel(
            file_path,
            header_row=1
        )

    return core_data


# ----------------------------------------------------------
# Load Supporting Files
# Supporting datasets use header row = 0
# ----------------------------------------------------------

def load_supporting_files():

    supporting_data = {}

    print("\nLoading Supporting Files...\n")

    for dataset_name, file_name in SUPPORTING_FILES.items():

        file_path = SUPPORTING_DATA_DIR / file_name

        # Supporting datasets have headers on first row
        supporting_data[dataset_name] = load_excel(
            file_path,
            header_row=0
        )

    return supporting_data


# ----------------------------------------------------------
# Display Dataset Summary
# ----------------------------------------------------------

def show_dataset_info(data_dictionary):

    print("\nDataset Summary")
    print("-" * 70)

    for dataset_name, dataframe in data_dictionary.items():

        if dataframe is not None:

            print(
                f"{dataset_name:<20}"
                f" Rows : {dataframe.shape[0]:>6}"
                f" Columns : {dataframe.shape[1]:>4}"
            )

        else:

            print(f"{dataset_name:<20} Not Loaded")


# ----------------------------------------------------------
# Print Dataset Columns
# ----------------------------------------------------------

def print_dataset_columns(title, datasets):

    print("\n")
    print("=" * 70)
    print(title)
    print("=" * 70)

    for dataset_name, dataframe in datasets.items():

        print(f"\n{dataset_name}")
        print("-" * 70)

        if dataframe is not None:

            print(dataframe.columns.tolist())

        else:

            print("Dataset Not Loaded")


# ----------------------------------------------------------
# Analyze Dataset
# ----------------------------------------------------------

def analyze_dataset(dataset_name, dataframe):

    print("\n" + "=" * 70)
    print(f"DATASET : {dataset_name.upper()}")
    print("=" * 70)

    # Shape
    rows, cols = dataframe.shape

    print(f"Rows             : {rows}")
    print(f"Columns          : {cols}")

    # Duplicate Rows
    duplicates = dataframe.duplicated().sum()

    print(f"Duplicate Rows   : {duplicates}")

    # Missing Values
    missing = dataframe.isnull().sum().sum()

    print(f"Missing Values   : {missing}")

    # Memory Usage
    memory = dataframe.memory_usage(deep=True).sum() / 1024

    print(f"Memory Usage     : {memory:.2f} KB")

    # Column Names
    print("\nColumn Names")
    print("-" * 70)

    for column in dataframe.columns:

        print(column)

    # Data Types
    print("\nData Types")
    print("-" * 70)

    print(dataframe.dtypes)


# ----------------------------------------------------------
# Main Function
# ----------------------------------------------------------

def main():

    # ------------------------------------------------------
    # Load All Datasets
    # ------------------------------------------------------

    core_data = load_core_files()

    supporting_data = load_supporting_files()


    # ----------------------------------------------------------
    # Display Companies Dataset
    # ----------------------------------------------------------

    companies = core_data["companies"]

    print("\n" + "=" * 70)
    print("COMPANIES DATASET (FIRST 10 ROWS)")
    print("=" * 70)

    print(companies.head(10))
 
    print("\n" + "=" * 70)
    print("COMPANIES COLUMN NAMES")
    print("=" * 70)

    print(companies.columns.tolist())

    print("\n" + "=" * 70)
    print("FIRST 10 ROWS (FIRST 5 COLUMNS)")
    print("=" * 70)

    print(companies.iloc[:10, :5])

    # ------------------------------------------------------
    # Dataset Summary
    # ------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("CORE DATASETS")
    print("=" * 70)

    show_dataset_info(core_data)

    print("\n")
    print("=" * 70)
    print("SUPPORTING DATASETS")
    print("=" * 70)

    show_dataset_info(supporting_data)

    # ------------------------------------------------------
    # Print Column Names
    # ------------------------------------------------------

    print_dataset_columns(
        "CORE DATASET COLUMNS",
        core_data
    )

    print_dataset_columns(
        "SUPPORTING DATASET COLUMNS",
        supporting_data
    )

    # ------------------------------------------------------
    # Detailed Dataset Analysis
    # ------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("DETAILED DATASET ANALYSIS")
    print("=" * 70)

    # Analyze Core Datasets

    for dataset_name, dataframe in core_data.items():

        if dataframe is not None:

            analyze_dataset(
                dataset_name,
                dataframe
            )

    # Analyze Supporting Datasets

    for dataset_name, dataframe in supporting_data.items():

        if dataframe is not None:

            analyze_dataset(
                dataset_name,
                dataframe
            )


# ----------------------------------------------------------
# Run Program
# ----------------------------------------------------------

if __name__ == "__main__":

    main()