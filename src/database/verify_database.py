from src.database.database_utils import get_connection

connection = get_connection()
cursor = connection.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "financial_ratios",
    "market_cap",
    "stock_prices"
]

print("=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<20} {count} rows")

connection.close()