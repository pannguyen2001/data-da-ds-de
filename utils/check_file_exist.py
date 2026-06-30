import os
from .logger import other_common_logger

@other_common_logger.catch
def check_file_exist(file_path: str = "") -> bool:
    """
    Check if a file exists at the given path.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if not isinstance(file_path, str):
        other_common_logger.error(f"Invalid file path type: {file_path}, {type(file_path)}")
        return False

    if not os.path.exists(file_path):
        other_common_logger.error(f"File not found: {file_path}")
        return False

    other_common_logger.success(f"File found: {file_path}")
    return True