import polars as pl
from pydantic.dataclasses import dataclass

from src.io.reader.base import FileReader


@dataclass
class CsvReader(FileReader):
    def _do_load(self) -> pl.LazyFrame:
        return pl.scan_csv(self.config.file_path, encoding="utf8-lossy", **self.config.options)
