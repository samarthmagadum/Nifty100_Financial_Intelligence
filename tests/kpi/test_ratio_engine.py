import pandas as pd

from src.analytics.ratio_engine import get_cagr

df = pd.DataFrame({
    "sales": [100, 120, 150, 180, 220, 260],
    "net_profit": [10, 12, 15, 18, 21, 25],
    "eps": [2, 2.5, 3, 3.6, 4.1, 5]
})

print("=" * 60)
print("Revenue CAGR")
print("=" * 60)

value, flag = get_cagr(df, "sales", 5)

print("Flag :", flag)
print("Value:", value)

print("\nPAT CAGR")
print(get_cagr(df, "net_profit", 5))

print("\nEPS CAGR")
print(get_cagr(df, "eps", 5))