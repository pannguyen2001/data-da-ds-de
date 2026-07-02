from pathlib import Path

import polars as pl
from pydantic import BaseModel, ConfigDict
from pydantic import Field

from src.common.constants import OperationStatus
from src.models.metadata import MetaData


class ReaderResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: pl.LazyFrame | None
    source: Path
    col_count: int | None
    data_schema: pl.Schema | None
    status: OperationStatus
    metadata: MetaData = Field(default_factory=MetaData)
