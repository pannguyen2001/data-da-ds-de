from abc import ABC, abstractmethod
from typing import Any
import traceback
import datetime
import os

from pydantic.dataclasses import dataclass

from src.common.logger import logger
from src.models.config.file_config import FileConfig
from src.models.result.loader_result import LoaderResult
from src.common.constants import OperationStatus
from src.models.metadata import MetaData


@dataclass
class FileLoader(ABC):
    """Base class for file reader strategies."""

    config: FileConfig

    def validate(self) -> None:
        """Validate that the target file exists."""
        if not self.config.file_path.exists():
            raise FileNotFoundError(
                f"[{self.__class__.__name__}] File not found: {str(self.config.file_path)}"
            )
        if not self.config.file_path.is_file():
            raise ValueError(
                f"[{self.__class__.__name__}] Invalid file path: {str(self.config.file_path)}"
            )

        pass

    @abstractmethod
    def _do_load(self) -> Any:
        """Subclasses must implement this method to handle specific file parsing."""

        pass

    def load(self) -> LoaderResult:
        """
        The main entrypoint for reading data. Handles logging,
        validation, and error catching safely.
        """
        try:
            self.validate()

            logger.info(
                f"[{self.__class__.__name__}] Read data from file: {str(self.config.file_path)}."
            )

            data = self._do_load()
            data_size: float = round(os.path.getsize(self.config.file_path) / 1024 / 1024, 4)

            logger.info(f"[{self.__class__.__name__}] Read data complete.")

            return LoaderResult(
                data=data,
                source=self.config.file_path,
                size_mb=data_size,
                status=OperationStatus.PASS,
                error=None,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )

        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Error: {str(e)}.")
            tb = "\n".join(traceback.TracebackException.from_exception(e).format())
            return LoaderResult(
                data=None,
                status=OperationStatus.FAIL,
                source=self.config.file_path,
                size_mb=None,
                error=tb,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
