"""
config.py

This file stores all project paths and filenames.
If the project folder changes, you only need to update this file.
"""

from pathlib import Path

# --------------------------------------------------
# Get the root directory of the project
# Example:
# D:/Nifty100_Financial_Intelligence/
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------
# Data Folder Paths
# --------------------------------------------------

# Folder containing 7 core Excel files
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Folder containing 5 supporting Excel files
SUPPORTING_DATA_DIR = PROJECT_ROOT / "data" / "supporting"

# Folder where cleaned files will be stored
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# --------------------------------------------------
# Output Folder
# --------------------------------------------------

# Folder for logs, reports, validation files etc.
OUTPUT_DIR = PROJECT_ROOT / "output"

# --------------------------------------------------
# Database Folder
# --------------------------------------------------

DATABASE_DIR = PROJECT_ROOT / "db"

# SQLite database file
DATABASE_PATH = DATABASE_DIR / "nifty100.db"

# --------------------------------------------------
# Core Dataset Names
# --------------------------------------------------

CORE_FILES = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
}

# --------------------------------------------------
# Supporting Dataset Names
# --------------------------------------------------

SUPPORTING_FILES = {
    "financial_ratios": "financial_ratios.xlsx",
    "market_cap": "market_cap.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
}