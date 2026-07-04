import polars as pl
from pydantic.dataclasses import dataclass

from src.common.reader.base import FileReader


@dataclass
class SqlReader(FileReader):
    def execute(self) -> pl.LazyFrame:
        return pl.read_database_uri(**self.config.options).lazy()
