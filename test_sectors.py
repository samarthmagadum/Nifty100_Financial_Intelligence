import pandas as pd

df = pd.read_excel("data/supporting/sectors.xlsx")

print(df.columns.tolist())
print()
print(df.head())