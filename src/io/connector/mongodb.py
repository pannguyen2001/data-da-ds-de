from copy import deepcopy
from typing import Any
from bson import ObjectId

import polars as pl
from pydantic.dataclasses import dataclass
from pymongo import MongoClient

from src.common.logger import logger

from .base import DatabaseConnector


@dataclass
class MongoDbConnector(DatabaseConnector):

    def normalize(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, dict):
            return {
                k: self.normalize(v)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [self.normalize(v) for v in value]

        return value

    def connect(self) -> None:
        logger.info(
            f"[{self.__class__.__name__}] Connect to '{self.config.engine}' database: {self.config.connection_info.database}, collection: {self.config.connection_info.tb_or_collection}."
        )

        cfg = self.config.connection_info
        self.config.options = {} if self.config.options is None else self.config.options

        if self.config.connection_info.uri is not None:
            self.conn = MongoClient(cfg.uri, **self.config.options)
        else:
            self.conn = MongoClient(
                host=cfg.host,
                port=cfg.port,
                username=cfg.username,
                password=cfg.password,
                **self.config.options,
            )

        self.conn.admin.command("ping")

        if cfg.database not in self.conn.list_database_names():
            raise ValueError(f"Database '{cfg.database}' not found.")

        self.db = self.conn[cfg.database]

        logger.success(f"[{self.__class__.__name__}] Connect database '{cfg.database}', collection '{cfg.tb_or_collection}' successfully.")

    def execute(self, query: Any) -> pl.LazyFrame:
        try:
            if not self.config.connection_info.tb_or_collection:
                raise ValueError("Collection name is not specified.")

            if self.config.connection_info.tb_or_collection not in self.db.list_collection_names():
                raise ValueError(f"Collection '{self.config.connection_info.tb_or_collection}' not found in database '{self.config.connection_info.database}'.")

            self.collection = self.db[self.config.connection_info.tb_or_collection]

            if query is None:
                query = {}
            data = self.collection.find(query)

            docs: list = [self.normalize(doc) for doc in data]
            return pl.LazyFrame(docs)
        except Exception as e:
            raise e

    def close(self) -> None:
        self.conn.close()
        logger.success(f"[{self.__class__.__name__}] Close database connection.")
