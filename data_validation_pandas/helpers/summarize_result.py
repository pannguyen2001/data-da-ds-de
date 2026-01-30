import datetime
import pandas as pd
import numpy as np
from helpers.write_data_to_excel_file import write_data_to_excel_file
from loguru import logger

@logger.catch
def summarize_result(df: pd.DataFrame, file_path: str, sheet_name: str) -> None:
    """
    Summarize the result of data validation and write it to a new Excel file.
    """
    # Create a new DataFrame to store the summary
    df_summarize = df.copy()
    if df_summarize.empty:
        logger.warning("No data to summarize. Data has no issue.")
        return

    total_row = df_summarize.shape[0]
    df_summarize["Data samples"] = df_summarize[df_summarize.columns[0]] + " - Excel index: " + (df_summarize.index + 2).astype(str)

    df_summarize = df_summarize.explode("validation_result")
    df_summarize = df_summarize.groupby("validation_result").agg({"Data samples": list}).reset_index()

    df_summarize = df_summarize.rename({"validation_result": "Validation result"}, axis=1)

    df_summarize["Amount"] = df_summarize["Data samples"].map(lambda x: len(x))

    df_summarize = df_summarize.sort_values(by=["Amount"], ascending=False).reset_index(drop=True)

    df_summarize["Error percentage (%)"] = np.round(df_summarize["Amount"] / total_row, 4) * 100

    df_summarize["Amount"] = df_summarize["Amount"].astype(str) + " / " + str(total_row)

    df_summarize["Data samples"] = df_summarize["Data samples"].map(lambda x: x[:5] if len(x) > 5 else x)
    df_summarize["Data samples"] = df_summarize["Data samples"].map(lambda x: "\n".join(x))

    write_data_to_excel_file(df_summarize, file_path, sheet_name)