from src.etl.loader import load_core_files

data = load_core_files()

for table_name in ["balancesheet", "cashflow"]:

    df = data[table_name]

    print("\n" + "=" * 60)
    print(table_name.upper())
    print("=" * 60)

    exact_duplicates = df[df.duplicated(keep=False)]

    print("Exact Duplicate Rows:", len(exact_duplicates))

    if len(exact_duplicates) > 0:
        print(exact_duplicates.head(10))