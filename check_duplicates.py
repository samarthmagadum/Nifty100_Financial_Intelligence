from src.etl.loader import load_core_files

data = load_core_files()

tables = {
    "profitandloss": data["profitandloss"],
    "balancesheet": data["balancesheet"],
    "cashflow": data["cashflow"]
}

for name, df in tables.items():

    print("\n" + "="*60)
    print(name.upper())
    print("="*60)

    duplicates = df[df.duplicated(
        subset=["company_id", "year"],
        keep=False
    )]

    print("Duplicate Rows :", len(duplicates))

    if len(duplicates) > 0:
        print(duplicates[["company_id", "year"]].head(20))