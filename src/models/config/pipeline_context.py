from typing import Any

from pydantic import Field, ConfigDict
from pydantic.dataclasses import dataclass

from src.common.constants import OperationStatus
from src.io.connector.base import DatabaseConnector
from src.io.downloader.base import Downloader
from src.io.reader.base import FileReader
from src.models.metadata import MetaData


@dataclass
class PipelineContext:
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: dict[str, Any] = Field(default_factory=dict)
    readers: list[FileReader] = Field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = Field(default_factory=list)
    downloaders: list[Downloader] = Field(default_factory=list)

    metadata: MetaData = Field(default_factory=MetaData)
    status: OperationStatus = Field(default=OperationStatus.PENDING)
    report: dict[str, Any] = Field(default_factory=dict)
    checkpoint: dict[str, Any] = Field(default_factory=dict)
    error: Exception | str | None = None
