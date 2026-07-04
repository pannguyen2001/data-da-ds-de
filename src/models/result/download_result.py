from pydantic import BaseModel
from pathlib import Path
from pydantic import Field, ConfigDict

from src.models.metadata import MetaData
from src.common.constants import DownloadStatus


class DownloadResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    source: str
    destination: Path
    status: DownloadStatus
    files_downloaded: list[Path]
    duration_seconds: float
    error: Exception | str | None
    metadata: MetaData = Field(default_factory=MetaData)