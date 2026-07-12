import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import polars as pl
from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import DatetimeFormat, ResolveFileType
from src.models.config.db_connector_config import ConnectionInfo
from src.models.result.db_connector_result import DbConnectorResult
from src.models.result.reader_result import ReaderResult


class StorageConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    df: pl.LazyFrame | None
    des_folder_path: Path = Field(default_factory=Path)
    des_file_name: str = Field(
        default_factory=lambda: (
            f"unknown_{datetime.datetime.now().strftime(DatetimeFormat.DATETIME_YEAR_FIRST.value)}"
        )
    )
    options: dict[str, Any] | None = Field(default_factory=dict)
    mode: Literal["a", "w", "i"] = (
        "w"  # a: append, w: drop all and write, i: incremntal loader, default "w"
    )


@dataclass
class StorageConfigBuilder:
    file_type: ResolveFileType
    des_folder_path: Path

    def build(self, df: pl.LazyFrame | None, file_name: str) -> StorageConfig:
        """Build storage config."""

        return StorageConfig(
            df=df,
            des_folder_path=self.des_folder_path,
            des_file_name=file_name,
            mode="w",
            options=None,
        )

    def from_reader(self, result: ReaderResult) -> StorageConfig:
        """Config storage from reader result."""

        if result.sheet is not None:
            des_file_name = f"{result.source.stem}/{result.sheet}.{self.file_type}"
        else:
            folder_name = result.source.parent.name or "unknown"
            des_file_name = f"{folder_name}/{result.source.stem}.{self.file_type}"

        return self.build(result.data, des_file_name)

    def from_db(
        self, dbconnector_result: DbConnectorResult, connection_info: ConnectionInfo
    ) -> StorageConfig:
        """Config storage from db sources."""

        des_file_name = f"{connection_info.database}/{connection_info.tb_or_collection}.{self.file_type}"

        return self.build(dbconnector_result.data, des_file_name)

    def from_api(self) -> None:
        """Config storage from api sources."""

    def from_downloader(self) -> None:
        """Config storage from downloader sources."""
