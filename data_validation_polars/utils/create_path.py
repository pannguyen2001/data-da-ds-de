from pathlib import Path

def create_path(path: str) -> Path:
    """
    Create a path if it doesn't exist.

    Args:
        path (str): The path to create.

    Returns:
        Path: The created path.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path