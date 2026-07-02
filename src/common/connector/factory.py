from pydantic.dataclasses import dataclass
from pydantic import Field

from src.common.constants import DbEngine
from .base import DatabaseConnector
from src.models.config.source_config import SourceConfig
# from src.connectors.database.postgresql import PostgresqlConnector
# from src.connectors.database.duckdb import DuckDbConnector


# Only use if expect external plugins, or complex config, else use registry for simple config
@dataclass
class DatabaseConnectorFactory:

    _connector: dict[DbEngine, type[DatabaseConnector]] = Field(default_factory=dict)

    def register(self, connector_name: DbEngine, connector: DatabaseConnector) -> None:
        self._connector[connector_name] = connector

    def unregister(self, connector_name: DbEngine) -> None:
        if connector_name in self._connector:
            del self._connector[connector_name]
        else:
            raise ValueError(f"Connector '{connector_name}' not found.")

    def create(self, connector_name: DbEngine, config: SourceConfig) -> DatabaseConnector:
        connector_cls = self._connector.get(connector_name)

        if connector_cls is None:
            raise ValueError(
                f"Unknown connector '{connector_name}'. "
                f"Available: {', '.join(self._connector)}"
            )

        return connector_cls(config)


# dbconnetor_config = DatabaseConnectorFactory()
# dbconnetor_config.register(DbEngine.POSTGRESQL, PostgresqlConnector)
# dbconnetor_config.register(DbEngine.DUCKDB, DuckDbConnector)