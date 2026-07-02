from src.common.constants import DbEngine
from .postgresql import PostgresqlConnector
from .duckdb import DuckDbConnector
from .mongodb import MongoDbConnector


_DB_CONNECTORS = {
    DbEngine.POSTGRESQL: PostgresqlConnector,
    DbEngine.DUCKDB: DuckDbConnector,
    DbEngine.MONGODB: MongoDbConnector
}