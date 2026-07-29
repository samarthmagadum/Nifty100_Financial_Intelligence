import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(
        str(DB_PATH),
        check_same_thread=False
    )

@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    query = """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker]

    if year is not None:

        query += " AND year = ?"
        params.append(year)

    query += " ORDER BY year"

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    query = """
    SELECT *
    FROM sectors
    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[group_name]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_valuation(ticker):

    df = pd.DataFrame()
    

    return df


@st.cache_data(ttl=600)
def get_home_data(year):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[year]
    )

    conn.close()

    return df