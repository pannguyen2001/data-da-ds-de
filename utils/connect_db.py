import sqlite3
from loguru import logger
# from .logger import logger_wrapper
from .logger import other_common_logger

@other_common_logger.catch
def connect_db(db_file_path: str = ""):
    """
    Connect to the SQLite database.


    Args:
        db_file_path (str, optional): Sqlite db path. Defaults to db_file_path.
    """

    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect(db_file_path)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Start a transaction
    cursor.execute("BEGIN;")

    other_common_logger.info(f"Database created and connected successfully!")
    return connection, cursor

@other_common_logger.catch
def close_db(connection: sqlite3.Connection):
    """
    Close db connection
    """
    connection.close()
    other_common_logger.info(f"Database closed successfully!")
    return True
