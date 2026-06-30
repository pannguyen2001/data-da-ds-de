import sqlite3
import pandas as pd
# from .logger import logger_wrapper
from .logger import other_common_logger

@other_common_logger.catch
def read_db(
    cursor: sqlite3.Cursor,
    connection: sqlite3.Connection,
    db_file_path: str = "",
    query: str = "",
    is_fetch_all: bool = True,
    size: int = 0
    ):
    """
    """

    if not db_file_path:
        raise ValueError("db_file_path is required")
    if not query:
        raise ValueError("query is required")

    other_common_logger.info(f"Start reading data from database: {db_file_path}")
    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()
    cursor.execute(query)

    if is_fetch_all:
        df = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])
    else:
        df = pd.DataFrame(cursor.fetchmany(size), columns=[column[0] for column in cursor.description])

    if df.empty:
        raise ValueError("No data found")

    other_common_logger.info(f"Complete reading data from database: {db_file_path}")
    return df

