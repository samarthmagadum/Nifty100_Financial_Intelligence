from src.analytics.cagr import calculate_cagr

print("=" * 60)
print("TESTING NORMAL CAGR")
print("=" * 60)

value, flag = calculate_cagr(
    start_value=100,
    end_value=200,
    years=5
)

print("Flag     :", flag)
print("Expected : NORMAL")

print("Value    :", value)
print("Expected : 14.87")

print("\n" + "=" * 60)
print("DECLINE TO LOSS")
print("=" * 60)

value, flag = calculate_cagr(
    start_value=100,
    end_value=-50,
    years=5
)

print(flag)
print("Expected : DECLINE_TO_LOSS")

print(value)
print("Expected : None")

print("\n" + "=" * 60)
print("TURNAROUND")
print("=" * 60)

value, flag = calculate_cagr(
    start_value=-100,
    end_value=50,
    years=5
)

print(flag)
print("Expected : TURNAROUND")

print(value)
print("Expected : None")

print("\n" + "=" * 60)
print("BOTH NEGATIVE")
print("=" * 60)

value, flag = calculate_cagr(
    start_value=-100,
    end_value=-50,
    years=5
)

print(flag)
print("Expected : BOTH_NEGATIVE")

print(value)
print("Expected : None")

print("\n" + "=" * 60)
print("ZERO BASE")
print("=" * 60)

value, flag = calculate_cagr(
    start_value=0,
    end_value=100,
    years=5
)

print(flag)
print("Expected : ZERO_BASE")

print(value)
print("Expected : None")

print("\n" + "=" * 60)
print("INSUFFICIENT YEARS")
print("=" * 60)

value, flag = calculate_cagr(
    start_value=100,
    end_value=150,
    years=0
)

print(flag)
print("Expected : INSUFFICIENT")

print(value)
print("Expected : None")