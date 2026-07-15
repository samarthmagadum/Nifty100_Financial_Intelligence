"""
This file is used only for testing.

Later we will replace it with proper pytest unit tests.
"""

# Import functions
from src.etl.normaliser import normalize_ticker
from src.etl.normaliser import normalize_year

print("Ticker Tests")
print("----------------------")

print(normalize_ticker(" tcs "))
print(normalize_ticker("infy"))
print(normalize_ticker(" Reliance "))

print()

print("Year Tests")
print("----------------------")

print(normalize_year("Mar-23"))
print(normalize_year("Dec-24"))
print(normalize_year("Mar-21"))
print(normalize_year("2023"))