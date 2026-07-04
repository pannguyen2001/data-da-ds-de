from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass
from typing import Any

import polars as pl

from src.models.config.db_connector_config import DbConfig
from src.common.logger import logger


@dataclass
class DatabaseConnector(ABC):

    config: DbConfig
    conn: Any | None = None
    cur: Any | None = None

    @abstractmethod
    def connect(self) -> Any:
        """Connect to the database."""

        ...

    @abstractmethod
    def execute(self, query: str) -> pl.LazyFrame:
        """Execute a query and return the result as a DataFrame."""

        ...

    @abstractmethod
    def close(self) -> None:
        """Close the connection to the database."""

        ...

    def run(self, query: Any) -> pl.LazyFrame:
        """Run a query and return the result."""

        self.connect()

        try:
            return self.execute(query)
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Error: {str(e)}.")

            raise e
        finally:
            self.close()