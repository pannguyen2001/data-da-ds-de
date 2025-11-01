import sqlite3
import pandas as pd
from typing import List
# from .logger import logger_wrapper
from .logger import other_common_logger
from .normalize_string import normalize_string

@other_common_logger.catch
def excel_to_sql(
    cursor: sqlite3.Cursor,
    connection: sqlite3.Connection,
    excel_file_path: str = "",
    is_all_sheet: bool = True,
    sheet_name_list: List = [],
    writing_type: str = "delete_and_insert"
    ):
    """_summary_

    Args:
        excel_file_path (str): Excel file path,
        table_name (str): Sheet name need to input to sqlite as table.
        connection (sqlite3.Connection): Connection to sqlite database.
        writing_type (str): Type to write data to excel file. If delete_and_insert: delete all rows and insert data. If cdc: do change data capture: add version, created_at, updated_at,..
    """
    if not excel_file_path:
        raise ValueError("Excel file path is empty")
    if not is_all_sheet and not sheet_name_list:
        raise ValueError("sheet_name_list can not be empty if is_all_sheet is False")

    if is_all_sheet:
        df = pd.ExcelFile(excel_file_path, engine="calamine")
        sheet_name_list = df.sheet_names

    other_common_logger.info(f"Start to read data from excel file: {excel_file_path}, sheet names: {sheet_name_list}")
    for sheet_name in sheet_name_list:
        df_sheet = pd.read_excel(excel_file_path, sheet_name)

        if  df_sheet.empty:
            raise ValueError("Excel file is empty")

        sheet_name = normalize_string(sheet_name)
        df_sheet.columns = [normalize_string(col) for col in df_sheet.columns]

        # Check if table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{sheet_name}'")
        table_exists = cursor.fetchone()

        # if delete_before_insert:
        # check exist table: delete all row => insert new row
        # if cdc:
        # check exist table: update data => insert new row
        # add created_at and updated_at column
        # add version column: 1/2/3/...
        # after update version, have table to show history:
        # table | version | file_path | file_type | sheet_name | created_at | updated_at | status | type (update, delete and insert)

        if table_exists:
            if writing_type == "delete_and_insert":
                cursor.execute(f"DELETE FROM {sheet_name}")
                connection.commit()
                other_common_logger.info(f"Data has been deleted from table: {sheet_name}")
        else:
            other_common_logger.info(f"Table: {sheet_name} does not exist, create new table")

        df_sheet.to_sql(sheet_name, connection, if_exists='replace', index=False)
        other_common_logger.info(f"Data has been inserted into table: {sheet_name}")

    return True