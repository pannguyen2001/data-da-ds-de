import sqlite3
import pandas as pd
# from .logger import logger_wrapper
from .logger import other_common_logger
from .normalize_string import normalize_string

@other_common_logger.catch
def json_to_sql(connection: sqlite3.Connection, json_file_path: str = "", table_name: str = ""):
    """_summary_

    Args:
        connection (sqlite3.Connection): _description_
        json_file_path (str, optional): _description_. Defaults to "".
        table_name (str, optional): _description_. Defaults to "".
    """
    
    if not json_file_path:
        raise ValueError("JSON file path is empty")
    
    if not table_name:
        table_name = json_file_path.split("/")[-1].split(".")[0]
        table_name = normalize_string(table_name)
        
    df = pd.read_json(json_file_path)
    
    if df.empty:
        raise ValueError("JSON file is empty")
    
    df.to_sql(table_name, connection, if_exists='replace', index=False)
    other_common_logger.info(f"Data has been inserted into table: {table_name}")
    return True