from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_cfo_quality_score,
    calculate_capex_intensity,
    calculate_fcf_conversion_rate,
    classify_capital_allocation
)


print("=" * 60)
print("TESTING FREE CASH FLOW")
print("=" * 60)

# Test 1
result = calculate_free_cash_flow(
    operating_activity=1200,
    investing_activity=-400
)

print("Expected : 800")
print("Actual   :", result)

# Test 2
result = calculate_free_cash_flow(
    operating_activity=600,
    investing_activity=-900
)

print("\nExpected : -300")
print("Actual   :", result)

# Test 3
result = calculate_free_cash_flow(
    operating_activity=0,
    investing_activity=0
)

print("\nExpected : 0")
print("Actual   :", result)


print("\n" + "=" * 60)
print("TESTING CFO QUALITY SCORE")
print("=" * 60)

# ------------------------
# Test 1
# ------------------------

cfo = [100,120,110,140,150]
pat = [80,100,90,120,130]

ratio, label = calculate_cfo_quality_score(cfo, pat)

print("Expected Ratio : 1.2")
print("Actual Ratio   :", ratio)

print("Expected Label : High Quality")
print("Actual Label   :", label)


# ------------------------
# Test 2
# ------------------------

cfo = [60,50,40,55,50]
pat = [100,100,100,100,100]

ratio, label = calculate_cfo_quality_score(cfo, pat)

print("\nExpected Label : Moderate")
print("Actual Label   :", label)


# ------------------------
# Test 3
# ------------------------

cfo = [20,30,15,10,25]
pat = [100,100,100,100,100]

ratio, label = calculate_cfo_quality_score(cfo, pat)

print("\nExpected Label : Accrual Risk")
print("Actual Label   :", label)


# ------------------------
# Test 4
# ------------------------

cfo = [100,100]
pat = [0,0]

ratio, label = calculate_cfo_quality_score(cfo, pat)

print("\nExpected : NO_DATA")
print("Actual   :", label)


print("\n" + "=" * 60)
print("TESTING CAPEX INTENSITY")
print("=" * 60)

value, label = calculate_capex_intensity(-200, 10000)

print("Expected :", 2.0)
print("Actual   :", value)

print("Expected :", "Asset Light")
print("Actual   :", label)

value, label = calculate_capex_intensity(-500, 10000)

print("\nExpected :", 5.0)
print("Actual   :", value)

print("Expected :", "Moderate")
print("Actual   :", label)

value, label = calculate_capex_intensity(-1200, 10000)

print("\nExpected :", 12.0)
print("Actual   :", value)

print("Expected :", "Capital Intensive")
print("Actual   :", label)


print("\n" + "=" * 60)
print("TESTING FCF CONVERSION")
print("=" * 60)

print(calculate_fcf_conversion_rate(500,1000))
print("Expected : 50.0")

print(calculate_fcf_conversion_rate(-300,600))
print("Expected : -50.0")

print(calculate_fcf_conversion_rate(100,0))
print("Expected : None")


print("\n" + "=" * 60)
print("TESTING CAPITAL ALLOCATION")
print("=" * 60)

print(classify_capital_allocation(100,-50,-20))
print("Expected : Reinvestor")

print(classify_capital_allocation(100,-50,-20,1.2))
print("Expected : Shareholder Returns")

print(classify_capital_allocation(100,50,-20))
print("Expected : Liquidating Assets")

print(classify_capital_allocation(-100,50,20))
print("Expected : Distress Signal")

print(classify_capital_allocation(-100,-50,20))
print("Expected : Growth Funded by Debt")

print(classify_capital_allocation(100,50,20))
print("Expected : Cash Accumulator")

print(classify_capital_allocation(-100,-50,-20))
print("Expected : Pre-Revenue")

print(classify_capital_allocation(100,-50,20))
print("Expected : Mixed")