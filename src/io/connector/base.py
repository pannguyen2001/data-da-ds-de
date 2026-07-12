import datetime
import traceback
from abc import ABC, abstractmethod
from typing import Any

import polars as pl
from pydantic.dataclasses import dataclass

from src.common.constants import OperationStatus
from src.common.logger import logger
from src.models.config.db_connector_config import DbConfig
from src.models.metadata import MetaData
from src.models.result.db_connector_result import DbConnectorResult


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

    def run(self, query: Any) -> DbConnectorResult:
        """Run a query and return the result."""

        try:
            self.connect()
            df = self.execute(query)
            return DbConnectorResult(
                data=df,
                error=None,
                status=OperationStatus.PASS,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Error: {str(e)}")
            tb = "\n".join(traceback.TracebackException.from_exception(e).format())
            return DbConnectorResult(
                data=None,
                error=tb,
                status=OperationStatus.FAIL,
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
        finally:
            self.close()
