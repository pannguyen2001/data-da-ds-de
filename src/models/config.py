from pathlib import Path
from typing import Any, Literal

import polars as pl
from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import ApiMethod, DbEngine, DownloadSource, SourceType


# ===== Api config =====
class ApiConfig(BaseModel):
    url: str
    method: ApiMethod
    options: dict[str, Any] | None = Field(default_factory=dict)


# ===== Db connector config =====
class ConnectionInfo(BaseModel):
    database: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None


class DbConfig(BaseModel):
    engine: DbEngine
    connection_info: ConnectionInfo
    query: Any | None = None
    options: dict[str, Any] | None = Field(default_factory=dict)


# ===== Download config =====


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


# ===== File config =====
class FileConfig(BaseModel):
    file_path: Path
    options: dict[str, Any] | None = Field(default_factory=dict)


# ===== Storage config =====
class StorageConfig(BaseModel):
    df: pl.LazyFrame | None
    des_file_path: Path = Field(default_factory=Path)
    options: dict[str, Any] | None = Field(default_factory=dict)
    mode: Literal["a", "w", "i"] = (
        "w"  # a: append, w: drop all and write, i: incremntal loader, default "w"
    )


# ===== Source config =====
class SourceConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    source_type: SourceType
    config: FileConfig | ApiConfig | DbConfig

    # TODO: Add mode: a: append, w: replace and write, o: onetime only load, i: incremental load
