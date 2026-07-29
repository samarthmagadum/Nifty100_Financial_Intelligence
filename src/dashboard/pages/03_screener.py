import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]

sys.path.append(
    str(PROJECT_ROOT)
)


from src.utils.data_utils import clean_dataframe


DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"



# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Stock Screener",
    layout="wide"
)


st.title("🔍 Stock Screener")



# =====================================================
# PRESET FILTERS
# =====================================================

st.sidebar.header(
    "🎯 Screener Filters"
)


preset = st.sidebar.selectbox(

    "Choose Preset",

    [
        "Custom",
        "Quality",
        "Value",
        "Growth",
        "Dividend",
        "Debt-Free",
        "Turnaround"
    ]

)



# =====================================================
# DEFAULT VALUES
# =====================================================

roe_default = 0.0
de_default = 5.0
fcf_default = -5000.0
revenue_default = -20.0
pat_default = -20.0
opm_default = 0.0
pe_default = 200.0
pb_default = 20.0
dividend_default = 0.0
icr_default = 0.0



# =====================================================
# PRESETS
# =====================================================


if preset == "Quality":

    roe_default = 20
    de_default = 1
    fcf_default = 0
    revenue_default = 10
    pat_default = 10
    opm_default = 10



elif preset == "Value":

    pe_default = 20
    pb_default = 3
    de_default = 1



elif preset == "Growth":

    roe_default = 15
    revenue_default = 15
    pat_default = 15



elif preset == "Dividend":

    dividend_default = 2



elif preset == "Debt-Free":

    de_default = 0



elif preset == "Turnaround":

    revenue_default = 5
    pat_default = 5
    fcf_default = 0



# =====================================================
# SLIDERS
# =====================================================


roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    0.0,
    50.0,
    roe_default
)


de_max = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    de_default
)


fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow (Cr)",
    -5000.0,
    10000.0,
    fcf_default
)


revenue_min = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    -20.0,
    50.0,
    revenue_default
)


pat_min = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    -20.0,
    50.0,
    pat_default
)


opm_min = st.sidebar.slider(
    "Minimum OPM (%)",
    0.0,
    60.0,
    opm_default
)


pe_max = st.sidebar.slider(
    "Maximum P/E",
    0.0,
    200.0,
    pe_default
)


pb_max = st.sidebar.slider(
    "Maximum P/B",
    0.0,
    20.0,
    pb_default
)


dividend_min = st.sidebar.slider(
    "Minimum Dividend Yield (%)",
    0.0,
    10.0,
    dividend_default
)


icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0,
    100.0,
    icr_default
)



# =====================================================
# LOAD DATA
# =====================================================


conn = sqlite3.connect(
    str(DB_PATH)
)


query = """

SELECT

fr.company_id,

c.company_name,

s.broad_sector,

fr.return_on_equity_pct,

fr.debt_to_equity,

fr.free_cash_flow_cr,

fr.revenue_cagr_5yr,

fr.pat_cagr_5yr,

fr.operating_profit_margin_pct,

fr.interest_coverage,

fr.composite_quality_score,

mc.pe_ratio,

mc.pb_ratio,

mc.dividend_yield_pct


FROM financial_ratios fr


LEFT JOIN companies c

ON fr.company_id = c.id


LEFT JOIN sectors s

ON fr.company_id = s.company_id


LEFT JOIN market_cap mc

ON fr.company_id = mc.company_id


AND CAST(substr(fr.year,-4) AS INTEGER)=mc.year


WHERE fr.year='Mar 2024'

"""


df = pd.read_sql(

    query,

    conn

)


conn.close()



# =====================================================
# CLEAN DATA
# =====================================================


df = clean_dataframe(df)



numeric_columns = [

    "return_on_equity_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "operating_profit_margin_pct",

    "interest_coverage",

    "pe_ratio",

    "pb_ratio",

    "dividend_yield_pct",

    "composite_quality_score"

]


for col in numeric_columns:

    df[col] = pd.to_numeric(

        df[col],

        errors="coerce"

    )



df[numeric_columns] = (

    df[numeric_columns]

    .fillna(0)

)



# =====================================================
# FILTER
# =====================================================


filtered_df = df[

    (df.return_on_equity_pct >= roe_min) &

    (df.debt_to_equity <= de_max) &

    (df.free_cash_flow_cr >= fcf_min) &

    (df.revenue_cagr_5yr >= revenue_min) &

    (df.pat_cagr_5yr >= pat_min) &

    (df.operating_profit_margin_pct >= opm_min) &

    (df.pe_ratio <= pe_max) &

    (df.pb_ratio <= pb_max) &

    (df.dividend_yield_pct >= dividend_min) &

    (df.interest_coverage >= icr_min)

]



# =====================================================
# RESULT HANDLING
# =====================================================


st.subheader(
    "📋 Screener Results"
)



if filtered_df.empty:

    st.warning(

        "No companies match your selected filters. Try relaxing the conditions."

    )

    st.stop()



display_df = filtered_df[

[

"company_id",

"company_name",

"broad_sector",

"return_on_equity_pct",

"debt_to_equity",

"free_cash_flow_cr",

"revenue_cagr_5yr",

"pat_cagr_5yr",

"operating_profit_margin_pct",

"pe_ratio",

"pb_ratio",

"dividend_yield_pct",

"interest_coverage",

"composite_quality_score"

]

]



display_df = display_df.rename(

columns={

"company_id":"Company ID",

"company_name":"Company Name",

"broad_sector":"Sector",

"return_on_equity_pct":"ROE %",

"debt_to_equity":"D/E",

"free_cash_flow_cr":"FCF (Cr)",

"revenue_cagr_5yr":"Revenue CAGR %",

"pat_cagr_5yr":"PAT CAGR %",

"operating_profit_margin_pct":"OPM %",

"pe_ratio":"P/E",

"pb_ratio":"P/B",

"dividend_yield_pct":"Dividend Yield %",

"interest_coverage":"ICR",

"composite_quality_score":"Composite Score"

}

)



display_df = display_df.sort_values(

    "Composite Score",

    ascending=False

)



st.success(

    f"✅ {len(display_df)} companies match your filters"

)



csv = display_df.to_csv(

    index=False

).encode("utf-8")



st.download_button(

    "📥 Download Filtered Results",

    csv,

    "nifty100_screener_results.csv",

    "text/csv"

)



st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True

)