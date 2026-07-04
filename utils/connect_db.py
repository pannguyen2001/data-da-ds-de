import sqlite3

from .logger import other_common_logger as logger


@logger.catch
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

    logger.info("Database created and connected successfully!")
    return connection, cursor


@logger.catch
def close_db(connection: sqlite3.Connection):
    """
    Close db connection
    """
    connection.close()
    logger.info("Database closed successfully!")
    return True
