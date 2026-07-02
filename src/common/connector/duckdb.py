import duckdb
import polars as pl
from pydantic.dataclasses import dataclass

from src.common.logger import logger

from .base import DatabaseConnector


@dataclass
class DuckDbConnector(DatabaseConnector):
    def connect(self) -> None:
        logger.info(
            f"[{self.__class__.__name__}] Connect to '{self.config.engine}' database: {self.config.connection_info.database}."
        )
        self.conn = duckdb.connect(
            **self.config.connection_info.model_dump(exclude_none=True),
            **self.config.options,
        )
        logger.success(f"[{self.__class__.__name__}] Connect database successfully.")

    def execute(self, query: str) -> pl.LazyFrame:
        return self.conn.execute(query).pl(lazy=True)

    def close(self) -> None:
        self.conn.close()
        logger.success(f"[{self.__class__.__name__}] Close database connection.")
