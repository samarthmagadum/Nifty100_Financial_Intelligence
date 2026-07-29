# Sprint 4 Retrospective

## Overview

Sprint 4 focused on completing the Nifty100 Financial Intelligence Platform dashboard, integrating analytics modules, performing quality testing, and improving user experience.


---

# Completed Work


## Dashboard Screens

Completed 8 Streamlit screens:


1. Home Dashboard

2. Company Profile

3. Stock Screener

4. Peer Comparison

5. Trend Analysis

6. Sector Analysis

7. Capital Allocation Map

8. Annual Reports



---

# UX Decisions


## 1. Interactive Visualization

Plotly was selected for charts because it provides:


- Interactive graphs
- Hover information
- Better exploration experience
- Dynamic filtering


Implemented charts:


- Bar charts
- Line charts
- Radar charts
- Bubble charts
- Treemap visualization



---


## 2. Streamlit Wide Layout


The dashboard uses:

layout="wide"



Benefits:


- Better chart visibility
- Supports large tables
- Improved dashboard readability



---


## 3. Filter-Based Navigation


Dropdowns and sliders were implemented for:


- Company selection
- Peer group selection
- Sector filtering
- Screener customization



This allows users to explore financial data easily.



---

# Data Edge Cases Discovered


## 1. Missing Financial Values


### Issue:

Some companies contained missing values in financial metrics.


Examples:

- ROE
- Debt/Equity
- Free Cash Flow
- CAGR values


### Solution:

Implemented:


- NULL handling
- NaN replacement
- N/A display
- Safe calculations



---


## 2. Partial Historical Data


### Issue:

Some companies had fewer than 10 years of financial history.


### Solution:


- Display available years
- Prevent chart crashes
- Show available data only



---


## 3. Duplicate Records


### Issue:


Duplicate company-year records were found during validation.


### Solution:


- Data quality checks added
- Duplicate validation performed
- Cleaned datasets used



---


## 4. Missing Annual Reports


### Issue:


Some companies did not have valid PDF report links.


### Solution:


- URL validation added
- Report unavailable badge displayed
- Invalid links handled safely



---

# Performance Findings


## Database Optimization


Implemented:


- Streamlit caching
- Reduced repeated database connections
- Optimized SQL queries



---


## Dashboard Performance


Results:


- Faster page loading
- Reduced database overhead
- Stable chart rendering
- Improved user experience



---


# Challenges Faced


## Database Schema Differences


Issue:


Different tables had different column names.


Examples:


- sector column differences
- market cap column differences
- company identifier mapping


Solution:


- Schema inspection
- SQL query correction
- Safe joins



---


## Missing Data Handling


Issue:


Missing values caused chart and table failures.


Solution:


- Added validation
- Added fillna handling
- Added error prevention



---

# Sprint Outcome


Sprint 4 successfully delivered:


✅ Complete Streamlit dashboard

✅ Financial intelligence modules

✅ Interactive visualizations

✅ QA tested screens

✅ Documentation completed


---

# Final Status


Sprint 4: COMPLETED ✅