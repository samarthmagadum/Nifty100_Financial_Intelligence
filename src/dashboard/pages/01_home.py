import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

st.title("🏠 Home Dashboard")

year = st.sidebar.selectbox(
    "Select Year",
    [
        "Mar 2019",
        "Mar 2020",
        "Mar 2021",
        "Mar 2022",
        "Mar 2023",
        "Mar 2024"
    ]
)

conn = sqlite3.connect(str(DB_PATH))


query = """
SELECT

    fr.company_id,

    fr.return_on_equity_pct,

    fr.debt_to_equity,

    fr.revenue_cagr_5yr,

    fr.composite_quality_score,

    mc.pe_ratio

FROM financial_ratios fr

LEFT JOIN market_cap mc

ON fr.company_id = mc.company_id

AND CAST(substr(fr.year,-4) AS INTEGER) = mc.year

WHERE fr.year = ?
"""


df = pd.read_sql(query, conn, params=[year])




avg_roe = df["return_on_equity_pct"].mean()

median_pe = df["pe_ratio"].median()

median_de = df["debt_to_equity"].median()

total_companies = df["company_id"].nunique()

median_revenue = df["revenue_cagr_5yr"].median()

debt_free = (df["debt_to_equity"] == 0).sum()


col1, col2, col3 = st.columns(3)

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "Average ROE",
        f"{avg_roe:.2f}%"
    )

with col2:
    st.metric(
        "Median P/E",
        f"{median_pe:.2f}"
    )

with col3:
    st.metric(
        "Median D/E",
        f"{median_de:.2f}"
    )

with col4:
    st.metric(
        "Total Companies",
        total_companies
    )

with col5:
    st.metric(
        "Median Revenue CAGR",
        f"{median_revenue:.2f}%"
    )

with col6:
    st.metric(
        "Debt-Free Companies",
        debt_free
    )


# =====================================================
# Sector Breakdown
# =====================================================

sector_query = """
SELECT *
FROM sectors
"""

sector_df = pd.read_sql(
    sector_query,
    conn
)

sector_count = (

    sector_df

    .groupby("broad_sector")

    .size()

    .reset_index(name="Companies")

)

fig = px.pie(

    sector_count,

    names="broad_sector",

    values="Companies",

    hole=0.5,

    title="Sector Breakdown"

)

fig.update_traces(

    textposition="inside",

    textinfo="percent+label"

)

fig.update_layout(

    height=500,

    legend_title="Sector"

)

st.plotly_chart(

    fig,

    use_container_width=True

)


top5_query = """
SELECT

    c.company_name,

    fr.company_id,

    fr.composite_quality_score

FROM financial_ratios fr

JOIN companies c

ON fr.company_id = c.id

WHERE fr.year = ?

ORDER BY fr.composite_quality_score DESC

LIMIT 5
"""

top5_df = pd.read_sql(
    top5_query,
    conn,
    params=[year]
)

st.subheader("🏆 Top 5 Companies by Composite Quality Score")

st.dataframe(
    top5_df,
    use_container_width=True
)
