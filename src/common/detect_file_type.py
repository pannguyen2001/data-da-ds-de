from pathlib import Path

from src.common.constants import FileType, ResolveFileType


def detect_file_type(file_path: Path) -> FileType:
    """
    Detects the file type of a given file path.

    Args:
        file_path (Path): The file path to detect the file type of.

    Returns:
        FileType: The detected file type.
    """

    suffix = file_path.suffix.lower().replace(".", "")

    match suffix:
        case FileType.YAML | FileType.YML:
            return ResolveFileType.YAML
        case FileType.JSON:
            return ResolveFileType.JSON
        case FileType.XLSX | FileType.XLS:
            return ResolveFileType.EXCEL
        case FileType.PARQUET:
            return ResolveFileType.PARQUET
        case FileType.CSV:
            return ResolveFileType.CSV
        case _:
            raise ValueError(
                f"[{detect_file_type.__name__}] Invalid file type: {suffix}."
            )
