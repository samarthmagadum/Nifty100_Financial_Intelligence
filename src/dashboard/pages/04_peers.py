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
    page_title="Peer Comparison",
    layout="wide"
)



# =====================================================
# CACHE DATABASE LOAD
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



st.title(
    "👥 Peer Comparison"
)



# =====================================================
# STEP 8
# PEER GROUP DROPDOWN
# =====================================================


peer_groups = load_data(
    """
    SELECT DISTINCT peer_group_name

    FROM peer_groups

    ORDER BY peer_group_name
    """
)



if peer_groups.empty:

    st.error(
        "No peer groups available"
    )

    st.stop()



selected_peer_group = st.selectbox(

    "Select Peer Group",

    peer_groups["peer_group_name"].tolist()

)



# =====================================================
# STEP 9
# LOAD COMPANIES
# =====================================================


peer_companies = load_data(

    """

    SELECT

    pg.company_id,

    c.company_name,

    pg.is_benchmark


    FROM peer_groups pg


    JOIN companies c

    ON pg.company_id=c.id


    WHERE pg.peer_group_name=?

    """,

    [selected_peer_group]

)



st.subheader(
    "Companies in Peer Group"
)



if peer_companies.empty:

    st.warning(
        "No companies found"
    )

    st.stop()



st.dataframe(

    peer_companies,

    use_container_width=True

)



# =====================================================
# STEP 10
# LOAD METRICS
# =====================================================


company_ids = peer_companies["company_id"].tolist()


placeholders = ",".join(

    ["?"] * len(company_ids)

)



peer_metrics = load_data(

f"""

SELECT


company_id,

year,

net_profit_margin_pct,

return_on_equity_pct,

debt_to_equity,

free_cash_flow_cr,

revenue_cagr_5yr,

pat_cagr_5yr,

composite_quality_score


FROM financial_ratios


WHERE company_id IN ({placeholders})


AND year=(

SELECT MAX(year)

FROM financial_ratios

)


""",

company_ids

)



if peer_metrics.empty:

    st.error(
        "No financial data available"
    )

    st.stop()



# =====================================================
# CLEAN DATA
# =====================================================


metric_columns=[


"net_profit_margin_pct",

"return_on_equity_pct",

"debt_to_equity",

"free_cash_flow_cr",

"revenue_cagr_5yr",

"pat_cagr_5yr",

"composite_quality_score"


]


for col in metric_columns:

    peer_metrics[col]=pd.to_numeric(

        peer_metrics[col],

        errors="coerce"

    )



peer_metrics[metric_columns]=(

    peer_metrics[metric_columns]

    .fillna(0)

)



st.subheader(
    "Financial Metrics"
)


st.dataframe(

    peer_metrics,

    use_container_width=True

)



# =====================================================
# DATA AVAILABILITY CHECK
# =====================================================


years_available = (

    peer_metrics["year"]

    .nunique()

)



if years_available < 10:

    st.info(

        f"📌 Financial data available for {years_available} year(s)"

    )



# =====================================================
# STEP 10
# PEER AVERAGE
# =====================================================


metrics=[


"return_on_equity_pct",

"net_profit_margin_pct",

"debt_to_equity",

"free_cash_flow_cr",

"revenue_cagr_5yr",

"pat_cagr_5yr",

"composite_quality_score"


]


peer_average = (

    peer_metrics[metrics]

    .mean()

)



st.subheader(
    "Peer Average"
)



st.dataframe(

    peer_average.reset_index()

    .rename(

        columns={

            "index":"Metric",

            0:"Average"

        }

    ),

    use_container_width=True

)



# =====================================================
# STEP 11
# RADAR CHART
# =====================================================


st.subheader(
    "📊 Company vs Peer Average"
)



selected_company = st.selectbox(

    "Select Company",

    peer_metrics["company_id"].tolist()

)



company_data = peer_metrics[

    peer_metrics["company_id"]

    == selected_company

]



company_values=(

    company_data[metrics]

    .iloc[0]

    .values

)



average_values=(

    peer_average

    .values

)



radar_labels=[

"ROE",

"NPM",

"D/E",

"FCF",

"Revenue CAGR",

"PAT CAGR",

"Composite Score"

]



fig=go.Figure()



fig.add_trace(

go.Scatterpolar(

r=company_values,

theta=radar_labels,

fill="toself",

name=selected_company

)

)



fig.add_trace(

go.Scatterpolar(

r=average_values,

theta=radar_labels,

fill="toself",

name="Peer Average"

)

)



fig.update_layout(

height=600,

polar=dict(

radialaxis=dict(

visible=True

)

)

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# =====================================================
# STEP 12
# TABLE
# =====================================================


st.subheader(
    "📋 Peer Comparison Table"
)



comparison_table = peer_metrics.copy()



comparison_table["Rank"]=(

comparison_table["composite_quality_score"]

.rank(

ascending=False,

method="dense"

)

.fillna(0)

.astype(int)

)



comparison_table=(

comparison_table

.sort_values(

"Rank"

)

)



benchmark_ids=(

peer_companies[

peer_companies["is_benchmark"]==1

]

["company_id"]

.tolist()

)



def highlight_benchmark(row):

    if row["company_id"] in benchmark_ids:

        return [

            "background-color: yellow"

        ] * len(row)


    return [

        ""

    ] * len(row)



styled_table=(

comparison_table

.style

.apply(

highlight_benchmark,

axis=1

)

)



st.dataframe(

styled_table,

use_container_width=True

)