from pathlib import Path

import polars as pl
from pydantic import BaseModel

from src.common.constants import ReaderStatus
from src.models.metadata import MetaData


class ReaderResult(BaseModel):
    data: pl.DataFrame | pl.LazyFrame | None
    source: Path
    col_count: int | None
    data_schema: pl.Schema | None
    status: ReaderStatus
    metadata: MetaData
