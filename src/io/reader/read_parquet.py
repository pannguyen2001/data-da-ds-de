import polars as pl
from pydantic.dataclasses import dataclass

from src.io.reader.base import FileReader


@dataclass
class ParquetReader(FileReader):
    def _do_load(self) -> pl.LazyFrame:
        return pl.scan_parquet(self.config.file_path, **self.config.options)
