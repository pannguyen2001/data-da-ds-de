import datetime
import os
import traceback
from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl
from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from src.common.constants import OperationStatus
from src.common.logger import logger
from src.models.config.storage_config import StorageConfig
from src.models.metadata import MetaData
from src.models.result.storage_result import StorageResult


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Storage(ABC):
    """Base class for file storage strategies."""

    config: StorageConfig
    des_file_path: Path = Field(default_factory=Path)

    def validate(self) -> None:
        """Subclasses must implement this method to handle specific file storage."""
        if self.config.df is None:
            raise ValueError(f"[{self.__class__.__name__}] No data to storage.")

        if self.config.options is None:
            self.config.options = {}

        if not self.config.des_folder_path.is_dir():
            raise ValueError(f"{self.config.des_folder_path} must be a directory.")

    @abstractmethod
    def _do_save(self) -> None:
        """Subclasses must implement this method to handle specific file storage."""

        ...

    def save(self) -> StorageResult:
        """The main entrypoint for storage data."""

        self.des_file_path: Path = (
            self.config.des_folder_path / self.config.des_file_name
        )

        try:
            logger.info(
                f"[{self.__class__.__name__}] Storage data to file: {str(self.des_file_path)}."
            )

            self.validate()

            self.des_file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            rows = self.config.df.select(pl.len()).collect().item()

            if rows == 0:
                logger.info(f"[{self.__class__.__name__}] No data to storage.")
                return StorageResult(
                    destination=self.des_file_path,
                    size_mb=None,
                    status=OperationStatus.PASS,
                    error="No data to storage",
                    metadata=MetaData(
                        end_at=datetime.datetime.now(datetime.timezone.utc)
                    ),
                )

            self._do_save()

            file_size = round(
                os.path.getsize(self.des_file_path) / 1024 / 1024, 4
            )  # Convert bytes to MB
            result = StorageResult(
                destination=self.des_file_path,
                size_mb=file_size,
                status=OperationStatus.PASS,
                error=None,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )

            logger.info(f"[{self.__class__.__name__}] Storage data complete.")

            return result

        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Storage data failed: {e}.")
            tb = "\n".join(traceback.TracebackException.from_exception(e).format())
            return StorageResult(
                destination=self.des_file_path,
                size_mb=None,
                status=OperationStatus.FAIL,
                error=tb,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
