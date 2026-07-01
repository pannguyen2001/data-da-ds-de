import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

import polars as pl
from pydantic import Field
from pydantic.dataclasses import dataclass

from common.logger import logger
from models.reader_config import ReaderConfig
from src.common.constants import ReaderStatus
from src.models.metadata import MetaData
from src.models.reader_result import ReaderResult


@dataclass
class FileReader(ABC):
    """Base class for file reader strategies."""

    config: ReaderConfig = Field(default_factory=ReaderConfig)

    def validate(self, file_path: Path) -> None:
        """Validate that the target file exists."""
        if not file_path.exists():
            raise FileNotFoundError(
                f"[{self.__class__.__name__}] File not found: {str(file_path)}"
            )
        if not file_path.is_file():
            raise ValueError(
                f"[{self.__class__.__name__}] Invalid file path: {str(file_path)}"
            )

        pass

    @abstractmethod
    def _do_load(self) -> Union[pl.DataFrame, pl.LazyFrame]:
        """Subclasses must implement this method to handle specific file parsing."""
        pass

    def load(self) -> ReaderResult:
        """
        The main entrypoint for reading data. Handles logging,
        validation, and error catching safely.
        """

        logger.info(
            f"[{self.__class__.__name__}] Read data from file: {str(self.config.file_path)}."
        )
        self.validate(self.config.file_path)

        df = self._do_load()

        if df is None:
            result = ReaderResult(
                data=df,
                source=self.config.file_path,
                col_count=None,
                data_schema=None,
                status=ReaderStatus.FAIL,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
        else:
            result = ReaderResult(
                data=df,
                source=self.config.file_path,
                col_count=df.shape[1]
                if isinstance(df, pl.DataFrame)
                else len(df.collect_schema()),
                data_schema=df.collect_schema(),
                status=ReaderStatus.PASS,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )

        logger.info(f"[{self.__class__.__name__}] Read data complete.")

        return result
