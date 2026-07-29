import streamlit as st
import sqlite3
import pandas as pd
import requests
from pathlib import Path
from urllib.parse import urlparse



# =====================================================
# DATABASE PATH
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"



# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Annual Reports",

    layout="wide"

)



# =====================================================
# DATABASE CACHE
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
# CHECK URL
# =====================================================


@st.cache_data(ttl=3600)
def check_url(url):

    try:

        response = requests.head(

            url,

            timeout=5,

            allow_redirects=True

        )


        return response.status_code == 200


    except Exception:

        return False




# =====================================================
# TITLE
# =====================================================


st.title(
    "📄 Annual Reports"
)


st.write(
    "Company annual report repository"
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

        "No companies found"

    )

    st.stop()



selected_company = st.selectbox(

    "Search Company",

    companies["company_name"].tolist()

)



company_id = companies.loc[

    companies["company_name"]

    == selected_company,

    "id"

].iloc[0]



# =====================================================
# LOAD REPORTS
# =====================================================


reports = load_data(

"""

SELECT


year,

annual_report


FROM documents


WHERE company_id=?


ORDER BY year DESC


""",

[company_id]

)



st.subheader(

    f"{selected_company} Annual Reports"

)



if reports.empty:

    st.warning(

        "No annual reports available"

    )

    st.stop()



# =====================================================
# REPORT DISPLAY
# =====================================================


available_count = 0



for _, row in reports.iterrows():


    year = row["year"]

    url = row["annual_report"]



    st.markdown(

        f"### 📅 {year}"

    )



    # Missing URL

    if pd.isna(url) or str(url).strip()=="":


        st.error(

            "🔴 Report unavailable"

        )


        continue



    url=str(url).strip()



    # Invalid URL format

    parsed=urlparse(url)


    if not parsed.scheme:


        st.error(

            "🔴 Invalid report URL"

        )


        continue



    # Check PDF availability


    if check_url(url):


        available_count += 1


        st.success(

            "🟢 Report available"

        )


        st.markdown(

            f"""

            [📄 Open Annual Report PDF]({url})

            """

        )


    else:


        st.error(

            "🔴 Report unavailable"

        )



# =====================================================
# SUMMARY
# =====================================================


st.divider()


st.metric(

    "Available Reports",

    available_count

)