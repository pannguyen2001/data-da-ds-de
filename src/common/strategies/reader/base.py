from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from pydantic.dataclasses import dataclass
from pydantic import Field
from common.logger import logger


@dataclass
class FileReader(ABC):
    """Base class for reader strategies."""

    file_path: Path = Field(default_factory=Path)
    config: dict = Field(default_factory=dict)

    def validate(self) -> None:
        """Validate that the target file exists."""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"[{self.__class__.__name__}] File not found: {self.file_path}"
            )
        if not self.file_path.is_file():
            raise ValueError(
                f"[{self.__class__.__name__}] Invalid file path: {self.file_path}"
            )

    @abstractmethod
    def _do_load(self, *args, **kwargs) -> Any:
        """Subclasses must implement this method to handle specific file parsing."""
        pass

    def load(self, *args, **kwargs) -> Any:
        """
        The main entrypoint for reading data. Handles logging,
        validation, and error catching safely.
        """
        logger.info(
            "[%s] Read data from file: %s",
            self.__class__.__name__,
            self.file_path
        )
        self.validate()

        return self._do_load(*args, **kwargs)