from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic.dataclasses import dataclass

from common.logger import logger
from models.source_config import SourceConfig


@dataclass
class FileLoader(ABC):
    """Base class for file reader strategies."""

    config: SourceConfig

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
    def _do_load(self) -> Any:
        """Subclasses must implement this method to handle specific file parsing."""

        pass

    def load(self) -> Any:
        """
        The main entrypoint for reading data. Handles logging,
        validation, and error catching safely.
        """

        self.validate(self.config.file_path)

        logger.info(
            f"[{self.__class__.__name__}] Read data from file: {str(self.config.file_path)}."
        )

        data = self._do_load()

        logger.info(f"[{self.__class__.__name__}] Read data complete.")

        return data
