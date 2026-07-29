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
    page_title="Capital Allocation Map",
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
    "💰 Capital Allocation Map"
)


st.write(
    "Companies grouped by capital allocation behaviour"
)



# =====================================================
# LOAD DATA
# =====================================================


query = """

SELECT


c.company_name,


a.compounded_sales_growth,


a.compounded_profit_growth,


a.stock_price_cagr,


a.roe,


m.market_cap_crore



FROM analysis a



LEFT JOIN companies c

ON a.company_id=c.id



LEFT JOIN market_cap m

ON a.company_id=m.company_id



WHERE m.year=(

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
        "No capital allocation data found"
    )

    st.stop()



# =====================================================
# CLEAN DATA
# =====================================================


numeric_columns=[


"compounded_sales_growth",

"compounded_profit_growth",

"stock_price_cagr",

"roe",

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



df["company_name"]=df["company_name"].fillna(

    "Unknown Company"

)



# Remove duplicates

df=df.drop_duplicates(

subset=["company_name"]

)



# =====================================================
# CAPITAL PATTERN LOGIC
# =====================================================


def allocation_pattern(row):


    sales=row["compounded_sales_growth"]

    profit=row["compounded_profit_growth"]

    price=row["stock_price_cagr"]

    roe=row["roe"]



    if sales >= 15 and profit >= 15:

        return "High Growth"



    elif profit >= 15 and roe >= 15:

        return "Profit Compounder"



    elif roe >= 20 and price >= 15:

        return "Value Creator"



    elif sales >= 10 and roe >= 12:

        return "Stable Compounder"



    elif profit >= 20 and sales < 5:

        return "Turnaround"



    elif price >= 20:

        return "Market Favourite"



    elif sales < 5 and profit < 5:

        return "Slow Growth"



    else:

        return "Weak Allocation"



df["capital_pattern"]=df.apply(

    allocation_pattern,

    axis=1

)



# =====================================================
# TREEMAP
# =====================================================


st.subheader(
    "📊 Capital Allocation Treemap"
)



treemap_df=df.copy()



# avoid zero size issue

treemap_df["market_cap_crore"]=treemap_df[

"market_cap_crore"

].replace(

0,

1

)



fig=px.treemap(

    treemap_df,

    path=[

        "capital_pattern",

        "company_name"

    ],

    values="market_cap_crore",

    hover_data=[

        "roe",

        "compounded_sales_growth",

        "compounded_profit_growth"

    ],

    title="Companies grouped by Capital Allocation Pattern"

)



fig.update_layout(

    height=700

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# =====================================================
# PATTERN FILTER
# =====================================================


st.subheader(
    "Companies by Capital Pattern"
)



patterns=sorted(

    df["capital_pattern"]

    .unique()

)



selected_pattern=st.selectbox(

    "Select Pattern",

    patterns

)



pattern_df=df[

df["capital_pattern"]

==selected_pattern

]



st.dataframe(

    pattern_df[

    [

    "company_name",

    "capital_pattern",

    "compounded_sales_growth",

    "compounded_profit_growth",

    "stock_price_cagr",

    "roe",

    "market_cap_crore"

    ]

    ]

    .sort_values(

        by="market_cap_crore",

        ascending=False

    ),

    use_container_width=True,

    hide_index=True

)



# =====================================================
# SUMMARY
# =====================================================


st.subheader(
    "Pattern Summary"
)



summary=(

df.groupby(

"capital_pattern"

)

.agg(

Companies=(

"company_name",

"count"

),

Total_Market_Cap=(

"market_cap_crore",

"sum"

)

)

.reset_index()

)



st.dataframe(

summary,

use_container_width=True,

hide_index=True

)