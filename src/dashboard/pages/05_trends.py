import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# =====================================================
# DATABASE PATH
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"



# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)



# =====================================================
# CACHE DATABASE FUNCTION
# =====================================================

@st.cache_data(ttl=600)
def load_data(query, params=None):

    conn = sqlite3.connect(
        str(DB_PATH)
    )

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df



# =====================================================
# TITLE
# =====================================================

st.title(
    "📈 Trend Analysis"
)



# =====================================================
# COMPANY SEARCH
# =====================================================


companies = load_data(

"""
SELECT

id,

company_name

FROM companies

ORDER BY company_name

"""

)



if companies.empty:

    st.error(
        "No companies available"
    )

    st.stop()



company = st.selectbox(

    "Search Company",

    companies["company_name"].tolist()

)



company_id = companies.loc[

    companies.company_name == company,

    "id"

].iloc[0]



# =====================================================
# METRICS
# =====================================================


metrics = {


"Revenue CAGR 5Y":
"revenue_cagr_5yr",


"PAT CAGR 5Y":
"pat_cagr_5yr",


"ROE":
"return_on_equity_pct",


"Net Profit Margin":
"net_profit_margin_pct",


"Debt Equity":
"debt_to_equity",


"Free Cash Flow":
"free_cash_flow_cr"


}



selected_metrics = st.multiselect(

    "Select Maximum 3 Metrics",

    list(metrics.keys()),

    max_selections=3

)



if not selected_metrics:

    st.info(
        "Select at least one metric to display trend."
    )

    st.stop()



# =====================================================
# LOAD FINANCIAL DATA
# =====================================================


df = load_data(

"""

SELECT


year,


revenue_cagr_5yr,


pat_cagr_5yr,


return_on_equity_pct,


net_profit_margin_pct,


debt_to_equity,


free_cash_flow_cr


FROM financial_ratios


WHERE company_id=?


ORDER BY year


""",

[company_id]

)



if df.empty:

    st.warning(

        "No historical data available for this company."

    )

    st.stop()



# Remove TTM

df=df[

df["year"]!="TTM"

]



# =====================================================
# DATA CLEANING
# =====================================================


numeric_cols=list(

metrics.values()

)



for col in numeric_cols:


    df[col]=pd.to_numeric(

        df[col],

        errors="coerce"

    )



df[numeric_cols]=(

    df[numeric_cols]

    .fillna(0)

)



# =====================================================
# PARTIAL DATA CHECK
# =====================================================


available_years=df["year"].nunique()



if available_years < 10:

    st.info(

        f"📌 Data available only for {available_years} years"

    )



# =====================================================
# TREND CHART
# =====================================================


fig=go.Figure()



for metric in selected_metrics:


    col=metrics[metric]


    fig.add_trace(

        go.Scatter(

            x=df["year"],

            y=df[col],

            mode="lines+markers",

            name=metric

        )

    )



fig.update_layout(

    title=f"{company} Trend Analysis",

    xaxis_title="Year",

    yaxis_title="Value",

    height=600

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# =====================================================
# YOY CHANGE
# =====================================================


st.subheader(

    "📊 YoY Change %"

)



yoy=df.copy()



for metric in selected_metrics:


    col=metrics[metric]


    yoy[f"{metric} YoY %"]=(

        df[col]

        .pct_change()

        .replace(

            [float("inf"), -float("inf")],

            0

        )

        .fillna(0)

        *100

    )



display_cols=[

"year"

]


for metric in selected_metrics:

    display_cols.append(

        f"{metric} YoY %"

    )



st.dataframe(

    yoy[display_cols],

    use_container_width=True,

    hide_index=True

)