import os
import pandas as pd

def export_excel(results_dict):

    print()
    print("=" * 60)
    print("EXPORTING SCREENER EXCEL")
    print("=" * 60)

    os.makedirs("output", exist_ok=True)

    file_path = "output/screener_output.xlsx"

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

        for preset, df in results_dict.items():

            df.to_excel(
                writer,
                sheet_name=preset[:31],
                index=False
            )

    print()
    print("Excel Exported Successfully")
    print("File :", file_path)