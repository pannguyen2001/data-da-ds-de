import polars as pl
from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import DownloadStatus, OperationStatus
from src.models.metadata import MetaData


class DbConnectorResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: pl.LazyFrame | None
    status: OperationStatus | DownloadStatus
    error: Exception | str | None
    metadata: MetaData = Field(default_factory=MetaData)
