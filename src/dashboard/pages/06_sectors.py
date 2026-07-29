import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
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
    page_title="Sector Analysis",
    layout="wide"
)



# =====================================================
# DATABASE CACHE
# =====================================================

@st.cache_data(ttl=600)
def load_data(query):

    conn = sqlite3.connect(
        str(DB_PATH)
    )

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df



# =====================================================
# TITLE
# =====================================================


st.title(
    "🏭 Sector Analysis"
)


st.write(
    "Analyze companies based on sector performance"
)



# =====================================================
# LOAD DATA
# =====================================================


query = """

SELECT


c.company_name,


s.broad_sector,


s.sub_sector,


f.revenue_cagr_5yr,


f.return_on_equity_pct,


m.market_cap_crore



FROM companies c



LEFT JOIN sectors s

ON c.id=s.company_id



LEFT JOIN financial_ratios f

ON c.id=f.company_id



LEFT JOIN market_cap m

ON c.id=m.company_id



WHERE f.year=(

SELECT MAX(year)

FROM financial_ratios

)



AND m.year=(

SELECT MAX(year)

FROM market_cap

)

"""


df = load_data(query)



# =====================================================
# VALIDATION
# =====================================================


if df.empty:

    st.error(
        "No sector data available"
    )

    st.stop()



# Remove duplicate companies

df=df.drop_duplicates(

subset=[

"company_name"

]

)



# =====================================================
# DATA CLEANING
# =====================================================


numeric_columns=[

"revenue_cagr_5yr",

"return_on_equity_pct",

"market_cap_crore"

]


for col in numeric_columns:


    df[col]=pd.to_numeric(

        df[col],

        errors="coerce"

    )



df[numeric_columns]=(

    df[numeric_columns]

    .fillna(0)

)



# Replace missing text

df["broad_sector"]=df["broad_sector"].fillna(
    "Unknown"
)


df["sub_sector"]=df["sub_sector"].fillna(
    "Unknown"
)



# =====================================================
# SECTOR DROPDOWN
# =====================================================


sector_list=sorted(

    df["broad_sector"]

    .unique()

)



selected_sector=st.selectbox(

    "Select Sector",

    sector_list

)



sector_df=df[

df["broad_sector"]

==

selected_sector

]



if sector_df.empty:

    st.warning(
        "No companies available in this sector"
    )

    st.stop()



# =====================================================
# BUBBLE CHART
# =====================================================


st.subheader(

f"{selected_sector} - Company Bubble Chart"

)



fig=px.scatter(

    sector_df,

    x="revenue_cagr_5yr",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_name",

    hover_data={

        "revenue_cagr_5yr":":.2f",

        "return_on_equity_pct":":.2f",

        "market_cap_crore":":.2f"

    },

    title="Revenue Growth vs ROE"

)



fig.update_layout(

    height=650

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# =====================================================
# SECTOR MEDIAN KPI
# =====================================================


st.subheader(

"📊 Sector Median KPI"

)



median_data=pd.DataFrame(

{

"Metric":[

"Revenue CAGR 5Y",

"ROE",

"Market Cap"

],


"Median":[


sector_df[

"revenue_cagr_5yr"

]

.median(),



sector_df[

"return_on_equity_pct"

]

.median(),



sector_df[

"market_cap_crore"

]

.median()


]

}

)



median_data["Median"]=median_data["Median"].fillna(0)



fig2=px.bar(

median_data,

x="Metric",

y="Median",

title="Sector Median Metrics"

)



fig2.update_layout(

height=400

)



st.plotly_chart(

fig2,

use_container_width=True

)



# =====================================================
# COMPANY TABLE
# =====================================================


st.subheader(

"Companies in Sector"

)



display_df=sector_df[

[

"company_name",

"sub_sector",

"revenue_cagr_5yr",

"return_on_equity_pct",

"market_cap_crore"

]

].sort_values(

by="market_cap_crore",

ascending=False

)



st.dataframe(

display_df,

use_container_width=True,

hide_index=True

)