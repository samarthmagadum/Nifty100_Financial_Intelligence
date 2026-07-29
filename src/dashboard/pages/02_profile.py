import streamlit as st
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path


# =====================================================
# PATH
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Company Profile",
    layout="wide"
)


# =====================================================
# DATABASE CACHE FUNCTION
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
# HELPER
# =====================================================

def format_metric(value, suffix=""):

    if value is None or pd.isna(value):

        return "N/A"

    try:

        return f"{float(value):.2f}{suffix}"

    except:

        return "N/A"



# =====================================================
# TITLE
# =====================================================

st.title("🏢 Company Profile")



# =====================================================
# COMPANY LIST
# =====================================================


company_query = """

SELECT

id,
company_name

FROM companies

ORDER BY company_name

"""


companies = load_data(
    company_query
)



company_options = []


for _, row in companies.iterrows():

    company_options.append(
        f"{row['company_name']} ({row['id']})"
    )



selected_company = st.selectbox(

    "Search Company",

    company_options

)



ticker = (
    selected_company
    .split("(")[-1]
    .replace(")","")
)



# =====================================================
# COMPANY INFORMATION
# =====================================================


company_query = """

SELECT

c.id,

c.company_name,

c.about_company,

c.website,

c.roce_percentage,

c.roe_percentage,

s.broad_sector,

s.sub_sector


FROM companies c


LEFT JOIN sectors s

ON c.id=s.company_id


WHERE c.id=?

"""


company = load_data(

    company_query,

    [ticker]

)



if company.empty:

    st.error(
        "Ticker not found."
    )

    st.stop()



company = company.iloc[0]



st.subheader(
    "🏢 Company Information"
)



col1,col2 = st.columns(2)



with col1:

    st.write(
        "**Company Name**"
    )

    st.write(
        company["company_name"]
    )


    st.write(
        "**Ticker**"
    )

    st.write(
        company["id"]
    )


    st.write(
        "**Sector**"
    )

    st.write(
        company["broad_sector"]
        if pd.notna(company["broad_sector"])
        else "N/A"
    )


    st.write(
        "**Sub Sector**"
    )

    st.write(
        company["sub_sector"]
        if pd.notna(company["sub_sector"])
        else "N/A"
    )



with col2:

    st.write(
        "**Website**"
    )

    st.write(

        company["website"]
        if pd.notna(company["website"])
        else "N/A"

    )



st.subheader(
    "About Company"
)



about = company["about_company"]


if pd.isna(about):

    about="No description available."


st.write(
    about
)




# =====================================================
# KPI DATA
# =====================================================


kpi_query = """

SELECT

return_on_equity_pct,

net_profit_margin_pct,

debt_to_equity,

revenue_cagr_5yr,

free_cash_flow_cr


FROM financial_ratios


WHERE company_id=?

AND year='Mar 2024'

"""


kpi = load_data(

    kpi_query,

    [ticker]

)



if kpi.empty:


    kpi = pd.DataFrame(

        {

        "return_on_equity_pct":[None],

        "net_profit_margin_pct":[None],

        "debt_to_equity":[None],

        "revenue_cagr_5yr":[None],

        "free_cash_flow_cr":[None]

        }

    )



kpi=kpi.iloc[0]



# =====================================================
# KPI TILES
# =====================================================


st.subheader(
    "📊 Key Metrics"
)



c1,c2,c3 = st.columns(3)

c4,c5,c6 = st.columns(3)



with c1:

    st.metric(

        "ROE",

        format_metric(

            kpi["return_on_equity_pct"],

            "%"

        )

    )



with c2:

    st.metric(

        "ROCE",

        format_metric(

            company["roce_percentage"],

            "%"

        )

    )



with c3:

    st.metric(

        "Net Profit Margin",

        format_metric(

            kpi["net_profit_margin_pct"],

            "%"

        )

    )



with c4:

    st.metric(

        "Debt / Equity",

        format_metric(

            kpi["debt_to_equity"]

        )

    )



with c5:

    st.metric(

        "Revenue CAGR (5Y)",

        format_metric(

            kpi["revenue_cagr_5yr"],

            "%"

        )

    )



with c6:

    st.metric(

        "Free Cash Flow",

        format_metric(

            kpi["free_cash_flow_cr"],

            " Cr"

        )

    )



# =====================================================
# REVENUE PROFIT TREND
# =====================================================


pl_query="""

SELECT

year,

sales,

net_profit


FROM profitandloss


WHERE company_id=?


ORDER BY year

"""


pl_df=load_data(

    pl_query,

    [ticker]

)



pl_df=pl_df[

    pl_df["year"]!="TTM"

]



available_years = pl_df["year"].nunique()



if available_years < 10:

    st.info(

        f"📌 Data available only for {available_years} years"

    )



st.subheader(
    "Revenue & Net Profit Data"
)



if pl_df.empty:

    st.warning(
        "No revenue history available."
    )

else:


    st.dataframe(

        pl_df,

        use_container_width=True

    )


    plot_df=pl_df.melt(

        id_vars="year",

        value_vars=[

            "sales",

            "net_profit"

        ],

        var_name="Metric",

        value_name="Amount"

    )



    fig=px.bar(

        plot_df,

        x="year",

        y="Amount",

        color="Metric",

        barmode="group",

        title="Revenue vs Net Profit"

    )


    fig.update_layout(

        height=500

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# =====================================================
# ROE TREND
# =====================================================


roe_query="""

SELECT

year,

return_on_equity_pct


FROM financial_ratios


WHERE company_id=?


ORDER BY year

"""


roe_df=load_data(

    roe_query,

    [ticker]

)



roe_df=roe_df[

roe_df["year"]!="TTM"

]



st.subheader(
    "ROE Trend vs Current ROCE"
)



if roe_df.empty:


    st.warning(
        "ROE history not available."
    )


else:


    fig=go.Figure()



    fig.add_trace(

        go.Scatter(

            x=roe_df["year"],

            y=roe_df["return_on_equity_pct"],

            mode="lines+markers",

            name="ROE"

        )

    )


    fig.add_trace(

        go.Scatter(

            x=roe_df["year"],

            y=[company["roce_percentage"]]*len(roe_df),

            mode="lines",

            name="Current ROCE"

        )

    )


    fig.update_layout(

        height=500

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# =====================================================
# PROS AND CONS
# =====================================================


st.subheader(
    "✅ Pros & ❌ Cons"
)



pros_query="""

SELECT

pros,

cons


FROM prosandcons


WHERE company_id=?

"""


pros_df=load_data(

    pros_query,

    [ticker]

)



if pros_df.empty:


    st.info(
        "No Pros & Cons available."
    )


else:


    c1,c2=st.columns(2)


    with c1:

        st.success(
            "Pros"
        )

        for item in pros_df["pros"].dropna():

            st.write(
                f"✅ {item}"
            )



    with c2:

        st.error(
            "Cons"
        )

        for item in pros_df["cons"].dropna():

            st.write(
                f"❌ {item}"
            )