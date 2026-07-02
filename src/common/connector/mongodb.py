from copy import deepcopy
from typing import Any

import polars as pl
from pydantic.dataclasses import dataclass
from pymongo import MongoClient

from src.common.logger import logger

from .base import DatabaseConnector


@dataclass
class MongoDbConnector(DatabaseConnector):
    def connect(self) -> None:
        logger.info(
            f"[{self.__class__.__name__}] Connect to '{self.config.engine}' database: {self.config.connection_info.database}."
        )

        cfg = self.config.connection_info
        options = deepcopy(self.config.options)
        del options["collection"]

        self.conn = MongoClient(
            host=cfg.host,
            port=cfg.port,
            username=cfg.username,
            password=cfg.password,
            **self.config.options,
        )
        self.db = self.conn[cfg.database]

        logger.success(f"[{self.__class__.__name__}] Connect database successfully.")

    def execute(self, query: Any) -> pl.LazyFrame:
        collection = self.config.options.get("collection")
        if not collection:
            raise ValueError("Collection name is not specified.")

        self.collection = self.db[collection]
        data = self.collection.find(query)

        return pl.LazyFrame(list(data))

    def close(self) -> None:
        self.conn.close()
        logger.success(f"[{self.__class__.__name__}] Close database connection.")
