from pathlib import Path

from src.common.logger import logger


def create_io_entry(folder_path: str = "", file_name: str = "") -> Path:
    """
    Creates a folder, or a file within a folder, depending on input.

    Args:
        folder_path (str): Target directory path.
        file_name (str, optional): Target file name. If empty, only the folder is created.

    Returns:
        Path: The path to the created folder or file.
    """

    try:
        if not folder_path:
            raise ValueError("folder_path is required.")

        base_path = Path(folder_path)

        # Case 1: Folder only (file_name is empty)
        if not file_name:
            if base_path.exists():
                logger.warning(f"Folder already exists: {base_path}")
            else:
                base_path.mkdir(parents=True, exist_ok=True)
                logger.success(f"Folder created: {base_path}")
            return base_path

        # Case 2: File inside a folder
        file_path = base_path / file_name

        # Ensure the parent folders exist first (safe even if they do)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.exists():
            logger.warning(f"File already exists: {file_path}")
        else:
            file_path.touch()
            logger.success(f"File created: {file_path}")

        return file_path

    except Exception as e:
        logger.error(f"Error processing creation: {e}")
        raise
