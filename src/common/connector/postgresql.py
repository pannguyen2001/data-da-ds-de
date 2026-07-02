import polars as pl
import psycopg2
from pydantic.dataclasses import dataclass

from src.common.logger import logger

from .base import DatabaseConnector


@dataclass
class PostgresqlConnector(DatabaseConnector):
    def connect(self) -> None:
        logger.info(
            f"[{self.__class__.__name__}] Connect to '{self.config.engine}' database: {self.config.connection_info.database}."
        )

        self.conn = psycopg2.connect(
            **self.config.connection_info.model_dump(exclude_none=True),
            **self.config.options,
        )
        logger.success(f"[{self.__class__.__name__}] Connect database successfully.")

    def execute(self, query: str) -> pl.LazyFrame:
        with self.conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            return pl.LazyFrame(data)

    def close(self) -> None:
        with self.conn.cursor() as cur:
            cur.close()
        self.conn.close()
        logger.success(f"[{self.__class__.__name__}] Close database connection.")
