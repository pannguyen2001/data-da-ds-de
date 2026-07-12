import datetime
import traceback
from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl
from pydantic import Field
from pydantic.dataclasses import dataclass

from src.common.constants import OperationStatus, ResolveFileType
from src.common.detect_file_type import detect_file_type
from src.common.logger import logger
from src.models.config.file_config import FileConfig
from src.models.metadata import MetaData
from src.models.result.reader_result import ReaderResult


@dataclass
class FileReader(ABC):
    """Base class for file reader strategies."""

    config: FileConfig = Field(default_factory=FileConfig)

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
    def _do_load(self) -> pl.LazyFrame:
        """Subclasses must implement this method to handle specific file parsing."""

        pass

    def load(self) -> ReaderResult:
        """
        The main entrypoint for reading data. Handles logging,
        validation, and error catching safely.
        """

        self.validate(self.config.file_path)

        try:
            logger.info(
                f"[{self.__class__.__name__}] Read data from file: {str(self.config.file_path)}."
            )
            if self.config.file_type == ResolveFileType.EXCEL:
                sheet = self.config.options.get("sheet_name")
                logger.info(f"[{self.__class__.__name__}] sheet name: {sheet}.")
            else:
                sheet = None

            df = self._do_load()

            if df is None:
                result = ReaderResult(
                    data=df,
                    source=self.config.file_path,
                    sheet=sheet,
                    col_count=None,
                    data_schema=None,
                    status=OperationStatus.FAIL,
                    error="Data is None",
                    metadata=MetaData(
                        end_at=datetime.datetime.now(datetime.timezone.utc)
                    ),
                )
            else:
                result = ReaderResult(
                    data=df,
                    source=self.config.file_path,
                    sheet=sheet,
                    col_count=df.shape[1]
                    if isinstance(df, pl.DataFrame)
                    else len(df.collect_schema()),
                    data_schema=df.schema
                    if isinstance(df, pl.DataFrame)
                    else df.collect_schema(),
                    status=OperationStatus.PASS,
                    error=None,
                    metadata=MetaData(
                        end_at=datetime.datetime.now(datetime.timezone.utc)
                    ),
                )

            logger.info(f"[{self.__class__.__name__}] Read data complete.")

            return result
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Error reading data: {str(e)}")
            tb = "\n".join(traceback.TracebackException.from_exception(e).format())
            return ReaderResult(
                data=None,
                source=self.config.file_path,
                sheet=None,
                col_count=None,
                data_schema=None,
                status=OperationStatus.FAIL,
                error=tb,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
