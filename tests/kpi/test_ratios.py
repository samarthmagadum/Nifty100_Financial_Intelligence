from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    high_leverage_flag,
    calculate_interest_coverage,
    get_icr_label,
    icr_warning_flag,
    calculate_net_debt,
    calculate_asset_turnover
)


print("=" * 60)
print("TESTING NET PROFIT MARGIN")
print("=" * 60)

# Test 1
result = calculate_net_profit_margin(150, 1000)
print("Expected : 15.0")
print("Actual   :", result)

# Test 2
result = calculate_net_profit_margin(200, 500)
print("\nExpected : 40.0")
print("Actual   :", result)

# Test 3
result = calculate_net_profit_margin(100, 0)
print("\nExpected : None")
print("Actual   :", result)

# Test 4
result = calculate_net_profit_margin(-50, 1000)
print("\nExpected : -5.0")
print("Actual   :", result)



print("\n" + "=" * 60)
print("TESTING OPERATING PROFIT MARGIN")
print("=" * 60)

# Test 1
result = calculate_operating_profit_margin(250, 1000, 25)

print("Expected : 25.0")
print("Actual   :", result)

# Test 2
result = calculate_operating_profit_margin(250, 1000, 27)

print("\nExpected : Warning + 25.0")
print("Actual   :", result)

# Test 3
result = calculate_operating_profit_margin(250, 0)

print("\nExpected : None")
print("Actual   :", result)




print("\n" + "=" * 60)
print("TESTING RETURN ON EQUITY")
print("=" * 60)

# Test 1
result = calculate_roe(
    net_profit=500,
    equity_capital=100,
    reserves=900
)

print("Expected : 50.0")
print("Actual   :", result)

# Test 2
result = calculate_roe(
    net_profit=250,
    equity_capital=500,
    reserves=500
)

print("\nExpected : 25.0")
print("Actual   :", result)

# Test 3
result = calculate_roe(
    net_profit=100,
    equity_capital=0,
    reserves=0
)

print("\nExpected : None")
print("Actual   :", result)

# Test 4
result = calculate_roe(
    net_profit=100,
    equity_capital=-100,
    reserves=50
)

print("\nExpected : None")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING RETURN ON CAPITAL EMPLOYED")
print("=" * 60)

# Test 1
result = calculate_roce(
    operating_profit=800,
    other_income=50,
    interest=100,
    equity_capital=200,
    reserves=600,
    borrowings=700
)

print("Expected : 50.0")
print("Actual   :", result)

# Test 2
result = calculate_roce(
    operating_profit=500,
    other_income=20,
    interest=20,
    equity_capital=300,
    reserves=300,
    borrowings=400
)

print("\nExpected : 50.0")
print("Actual   :", result)

# Test 3
result = calculate_roce(
    operating_profit=500,
    other_income=0,
    interest=0,
    equity_capital=0,
    reserves=0,
    borrowings=0
)

print("\nExpected : None")
print("Actual   :", result)

# Test 4
result = calculate_roce(
    operating_profit=400,
    other_income=50,
    interest=100,
    equity_capital=-100,
    reserves=50,
    borrowings=20
)

print("\nExpected : None")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING RETURN ON ASSETS")
print("=" * 60)

# Test 1
result = calculate_roa(
    net_profit=400,
    total_assets=2000
)

print("Expected : 20.0")
print("Actual   :", result)

# Test 2
result = calculate_roa(
    net_profit=250,
    total_assets=1000
)

print("\nExpected : 25.0")
print("Actual   :", result)

# Test 3
result = calculate_roa(
    net_profit=100,
    total_assets=0
)

print("\nExpected : None")
print("Actual   :", result)

# Test 4
result = calculate_roa(
    net_profit=100,
    total_assets=-100
)

print("\nExpected : None")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING DEBT TO EQUITY")
print("=" * 60)

# Test 1
result = calculate_debt_to_equity(
    borrowings=500,
    equity_capital=100,
    reserves=900
)

print("Expected : 0.5")
print("Actual   :", result)

# Test 2
result = calculate_debt_to_equity(
    borrowings=0,
    equity_capital=100,
    reserves=900
)

print("\nExpected : 0")
print("Actual   :", result)

# Test 3
result = calculate_debt_to_equity(
    borrowings=100,
    equity_capital=0,
    reserves=0
)

print("\nExpected : None")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING HIGH LEVERAGE FLAG")
print("=" * 60)

# Test 1
print(high_leverage_flag(6.2, "Energy"))
print("Expected : True")

# Test 2
print(high_leverage_flag(6.2, "Financials"))
print("Expected : False")

# Test 3
print(high_leverage_flag(2.0, "Energy"))
print("Expected : False")


print("\n" + "=" * 60)
print("TESTING INTEREST COVERAGE RATIO")
print("=" * 60)

# Test 1
result = calculate_interest_coverage(
    operating_profit=1000,
    other_income=200,
    interest=300
)

print("Expected : 4.0")
print("Actual   :", result)

# Test 2
result = calculate_interest_coverage(
    operating_profit=1000,
    other_income=200,
    interest=0
)

print("\nExpected : None")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING ICR LABEL")
print("=" * 60)

print(get_icr_label(0))
print("Expected : Debt Free")

print(get_icr_label(250))
print("Expected : Normal")


print("\n" + "=" * 60)
print("TESTING ICR WARNING FLAG")
print("=" * 60)

print(icr_warning_flag(1.2))
print("Expected : True")

print(icr_warning_flag(2.5))
print("Expected : False")

print(icr_warning_flag(None))
print("Expected : False")


print("\n" + "=" * 60)
print("TESTING NET DEBT")
print("=" * 60)

# Test 1
result = calculate_net_debt(
    borrowings=1000,
    investments=300
)

print("Expected : 700")
print("Actual   :", result)

# Test 2
result = calculate_net_debt(
    borrowings=500,
    investments=800
)

print("\nExpected : -300")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING ASSET TURNOVER")
print("=" * 60)

# Test 1
result = calculate_asset_turnover(
    sales=8000,
    total_assets=4000
)

print("Expected : 2.0")
print("Actual   :", result)

# Test 2
result = calculate_asset_turnover(
    sales=5000,
    total_assets=2500
)

print("\nExpected : 2.0")
print("Actual   :", result)

# Test 3
result = calculate_asset_turnover(
    sales=5000,
    total_assets=0
)

print("\nExpected : None")
print("Actual   :", result)