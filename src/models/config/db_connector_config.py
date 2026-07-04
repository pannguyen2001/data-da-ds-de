from typing import Any

from pydantic import BaseModel, Field

from src.common.constants import DbEngine


class ConnectionInfo(BaseModel):
    database: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None


class DbConfig(BaseModel):
    engine: DbEngine
    connection_info: ConnectionInfo
    query: Any | None = None
    options: dict[str, Any] | None = Field(default_factory=dict)
