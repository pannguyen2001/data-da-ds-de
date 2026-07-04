from pydantic import BaseModel
from pathlib import Path
from typing import Literal

from src.common.constants import DownloadSource


class GGDriveOptions(BaseModel):
    item_type: Literal["file", "folder"] | None = None
    quiet: bool = False

class HuggingFaceOptions(BaseModel):
    file_name: str | None = None


class DownloadConfig(BaseModel):
    download_source_type: DownloadSource
    des_path: Path
    url: str = ""
    id: str = ""
    skip_existing: bool = True
    dry_run: bool = False
    overwrite: bool = False
    options: GGDriveOptions | HuggingFaceOptions | None = None