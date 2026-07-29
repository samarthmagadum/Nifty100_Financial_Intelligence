import pandas as pd


files = [
    "data/supporting/peer_groups.xlsx",
    "data/supporting/financial_ratios.xlsx",
    "data/supporting/market_cap.xlsx",
    "data/raw/profitandloss.xlsx",
    "data/raw/cashflow.xlsx"
]


for file in files:

    print("\n")
    print("="*60)
    print(file)
    print("="*60)


    df = pd.read_excel(file)

    print(df.columns.tolist())

    print(df.head(3))