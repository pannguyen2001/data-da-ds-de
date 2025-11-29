import sqlite3
import pandas as pd
# from .logger import logger_wrapper
from .logger import other_common_logger
from .normalize_string import normalize_string

@other_common_logger.catch
def csv_to_sql(connection: sqlite3.Connection, csv_file_path: str = "", table_name: str = "", is_index: bool = False):
    """_summary_

    Args:
        connection (sqlite3.Connection): _description_
        csv_file_path (str, optional): _description_. Defaults to "".
        is_index (bool, optional): _description_. Defaults to False.
    """

    if not table_name:
        table_name = csv_file_path.split("/")[-1].split(".")[0]
        table_name = normalize_string(table_name)

    df = pd.read_csv(csv_file_path)
    if  df.empty:
        raise ValueError("CSV file is empty")

    df.to_sql(table_name, connection, if_exists='replace', index=is_index)
    other_common_logger.info(f"Data has been inserted into table: {table_name}")
    return True