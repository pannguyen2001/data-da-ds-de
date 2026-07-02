from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic.dataclasses import dataclass, Field

from src.common.logger import logger


@dataclass
class FileLoader(ABC):
    """Base class for file reader strategies."""

    file_path: Path
    options: dict[str, Any] = Field(default_factory=dict)

    def validate(self) -> None:
        """Validate that the target file exists."""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"[{self.__class__.__name__}] File not found: {str(self.file_path)}"
            )
        if not self.file_path.is_file():
            raise ValueError(
                f"[{self.__class__.__name__}] Invalid file path: {str(self.file_path)}"
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

        self.validate()

        logger.info(
            f"[{self.__class__.__name__}] Read data from file: {str(self.file_path)}."
        )

        data = self._do_load()

        logger.info(f"[{self.__class__.__name__}] Read data complete.")

        return data
