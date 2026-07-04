from pathlib import Path
from typing import Any

import polars as pl
from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import DownloadStatus, OperationStatus
from src.models.metadata import MetaData


# ====== Base Result =====
class BaseResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: OperationStatus | DownloadStatus
    error: Exception | str | None
    metadata: MetaData = Field(default_factory=MetaData)


# ===== Connector result =====
class ConnectorResult(BaseResult):
    data: pl.LazyFrame | None
    size_mb: float | None


# ===== Download result =====
class DownloadResult(BaseResult):
    source: str
    destination: Path
    files_downloaded: list[Path]
    duration_seconds: float


# ===== Loader result =====
class LoaderResult(BaseResult):
    data: list | Any
    source: Path
    size_mb: float | None


# ===== Reader result =====
class ReaderResult(BaseResult):
    data: pl.LazyFrame | None
    source: Path
    col_count: int | None
    data_schema: pl.Schema | None


# ===== Storage result =====
class StorageResult(BaseResult):
    destination: Path
    size_mb: float | None
