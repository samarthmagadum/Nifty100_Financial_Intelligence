import os

import sqlite3

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from math import pi

from src.database.database_utils import get_connection

OUTPUT_FOLDER = "reports/radar_charts"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

def load_company_data():

    print()
    print("=" * 60)
    print("LOADING COMPANY DATA")
    print("=" * 60)

    conn = get_connection()

    query = """
    SELECT

        f.company_id,

        f.year,

        s.broad_sector,

        f.return_on_equity_pct,

        f.net_profit_margin_pct,

        f.debt_to_equity,

        f.free_cash_flow_cr,

        f.interest_coverage,

        f.asset_turnover,

        f.revenue_cagr_5yr,

        f.pat_cagr_5yr,

        f.composite_quality_score

    FROM financial_ratios f

    LEFT JOIN sectors s

    ON f.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print()
    print("Rows :", len(df))

    print()
    print("=" * 60)
    print("AVAILABLE COLUMNS")
    print("=" * 60)
    print(df.columns.tolist())

    return df

def normalize_metrics(df):

    print()
    print("=" * 60)
    print("NORMALIZING METRICS")
    print("=" * 60)

    metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
   ] 

    normalized_df = df.copy()

    for metric in metrics:

        minimum = normalized_df[metric].min()
        maximum = normalized_df[metric].max()

        if maximum != minimum:

            normalized_df[metric] = (
                (normalized_df[metric] - minimum)
                /
                (maximum - minimum)
            ) * 100

        else:

            normalized_df[metric] = 100

    return normalized_df

def create_radar_metrics(df):

    print()
    print("=" * 60)
    print("CREATING RADAR METRICS")
    print("=" * 60)


    # ROCE proxy
    # Using operating efficiency proxy because dataset has no ROCE

    df["roce_pct"] = (
        df["return_on_equity_pct"] *
        0.8
    )


    # FCF Score normalization proxy

    max_fcf = df["free_cash_flow_cr"].max()


    if max_fcf == 0:
        df["fcf_score"] = 0

    else:

        df["fcf_score"] = (
            df["free_cash_flow_cr"] /
            max_fcf
        ) * 100



    return df

def calculate_sector_average(df):

    print()
    print("=" * 60)
    print("CALCULATING SECTOR AVERAGES")
    print("=" * 60)


    metrics = [

    "return_on_equity_pct",     # ROE
    "roce_pct",                 # ROCE
    "net_profit_margin_pct",    # NPM
    "debt_to_equity",           # D/E
    "fcf_score",                # FCF Score
    "pat_cagr_5yr",             # PAT CAGR
    "revenue_cagr_5yr",         # Revenue CAGR
    "composite_quality_score"   # Composite Score

      ]


    sector_average = (
        df.groupby("broad_sector")[metrics]
        .mean()
        .reset_index()
    )


    print(sector_average)

    return sector_average


def generate_radar_chart(
        df,
        company_id,
        peer_avg,
        reference_type="Peer Average",
        output_dir="reports/radar_charts"
):

    import os
    import numpy as np
    import matplotlib.pyplot as plt


    os.makedirs(
        output_dir,
        exist_ok=True
    )


    company = df[
        df["company_id"] == company_id
    ]


    if company.empty:
        return



    # Latest year

    company = (
        company
        .sort_values("year")
        .tail(1)
    )


    metrics = [

        "return_on_equity_pct",
        "roce_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "fcf_score",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score"

    ]


    company_values = []
    peer_values = []



    for metric in metrics:


        company_value = company[
            metric
        ].iloc[0]


        peer_value = peer_avg[
            metric
        ]


        if pd.isna(company_value):
            company_value = 0


        if pd.isna(peer_value):
            peer_value = 0



        company_values.append(
            float(company_value)
        )


        peer_values.append(
            float(peer_value)
        )



    # Normalize

    max_values = np.maximum(
        company_values,
        peer_values
    )


    max_values[
        max_values == 0
    ] = 1



    company_norm = [
        x/y
        for x,y in zip(
            company_values,
            max_values
        )
    ]


    peer_norm = [
        x/y
        for x,y in zip(
            peer_values,
            max_values
        )
    ]



    # Close polygon

    company_norm.append(
        company_norm[0]
    )

    peer_norm.append(
        peer_norm[0]
    )


    angles = np.linspace(
        0,
        2*np.pi,
        len(metrics),
        endpoint=False
    )


    angles=np.append(
        angles,
        angles[0]
    )



    # Plot

    fig = plt.figure(
        figsize=(9,9)
    )


    ax = plt.subplot(
        111,
        polar=True
    )


    # Company polygon

    ax.plot(
        angles,
        company_norm,
        linewidth=2,
        label=company_id
    )


    ax.fill(
        angles,
        company_norm,
        alpha=0.25
    )



    # Peer average dashed

    ax.plot(
        angles,
        peer_norm,
        linestyle="--",
        linewidth=2,
        label=reference_type
    )



    ax.set_xticks(
        angles[:-1]
    )


    ax.set_xticklabels(
        [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF",
            "PAT CAGR",
            "Revenue CAGR",
            "Composite"
        ],
        fontsize=10
    )



    ax.set_title(
        f"{company_id} Financial Profile",
        fontsize=15,
        pad=25
    )


    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.3,1.1)
    )



    filename = os.path.join(
        output_dir,
        f"{company_id}_radar.png"
    )


    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


    print(
        f"Saved : {filename}"
    )

def generate_all_company_radar_charts(
        df,
        sector_average,
        output_dir="reports/radar_charts"
):

    import os
    import pandas as pd


    print()
    print("=" * 60)
    print("GENERATING RADAR CHARTS FOR ALL COMPANIES")
    print("=" * 60)


    os.makedirs(
        output_dir,
        exist_ok=True
    )


    companies = (
        df["company_id"]
        .dropna()
        .unique()
    )


    generated = []
    failed = []


    for company_id in companies:

        try:

            print()
            print(f"Processing : {company_id}")


            # Company sector

            company_sector = df[
                df["company_id"] == company_id
            ]["broad_sector"].iloc[0]


            # Sector average as fallback reference
            # (until peer_group column is available)

            peer_avg = sector_average[
                sector_average["broad_sector"] == company_sector
            ]


            if peer_avg.empty:

                # Nifty 100 average fallback

                peer_avg = df.mean(
                    numeric_only=True
                )

                reference_type = "Nifty 100 Average"


            else:

                peer_avg = peer_avg.iloc[0]

                reference_type = "Sector Average"



            # Generate chart

            generate_radar_chart(
                df=df,
                company_id=company_id,
                peer_avg=peer_avg,
                reference_type=reference_type,
                output_dir=output_dir
            )


            generated.append(
                company_id
            )


        except Exception as e:

            print(
                f"Failed : {company_id} -> {e}"
            )

            failed.append(
                company_id
            )



    print()
    print("=" * 60)
    print("RADAR GENERATION COMPLETED")
    print("=" * 60)


    print(
        f"Total Companies : {len(companies)}"
    )

    print(
        f"Charts Generated : {len(generated)}"
    )

    print(
        f"Failed : {len(failed)}"
    )


    log_df = pd.DataFrame(
        {
            "company_id": companies,
            "status": [
                "SUCCESS" if c in generated else "FAILED"
                for c in companies
            ]
        }
    )


    log_df.to_csv(
        "reports/radar_generation_log.csv",
        index=False
    )


    print(
        "Log Saved : reports/radar_generation_log.csv"
    )
    

def fix_missing_sectors(df):

    sector_mapping = {

        "ULTRACEMCO": "Materials",
        "UNIONBANK": "Financials",
        "UNITDSPR": "Consumer Staples",
        "VBL": "Consumer Staples",
        "VEDL": "Materials",
        "WIPRO": "Information Technology",
        "ZOMATO": "Consumer Discretionary",
        "ZYDUSLIFE": "Healthcare"

    }


    for company, sector in sector_mapping.items():

        df.loc[
            df["company_id"] == company,
            "broad_sector"
        ] = sector


    return df



if __name__ == "__main__":

    df = load_company_data()

    df = create_radar_metrics(df)

    df = fix_missing_sectors(df)

    df = normalize_metrics(df)

    sector_average = calculate_sector_average(df)


    company_id = "INFY"


    company_sector = df[
        df["company_id"] == company_id
    ]["broad_sector"].iloc[0]


    sector_avg = sector_average[
        sector_average["broad_sector"] == company_sector
    ].iloc[0]


    generate_all_company_radar_charts(
    df=df,
    sector_average=sector_average,
    output_dir="reports/radar_charts"
    )