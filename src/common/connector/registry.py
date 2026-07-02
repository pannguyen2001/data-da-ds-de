from src.common.connector.base import DatabaseConnector
from src.common.constants import DbEngine

from .duckdb import DuckDbConnector
from .mongodb import MongoDbConnector
from .postgresql import PostgresqlConnector

_DB_CONNECTORS: dict[DbEngine, type[DatabaseConnector]] = {
    DbEngine.POSTGRESQL: PostgresqlConnector,
    DbEngine.DUCKDB: DuckDbConnector,
    DbEngine.MONGODB: MongoDbConnector,
}
