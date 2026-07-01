import polars as pl
from pydantic.dataclasses import dataclass

from common.strategies.reader.base import FileReader


@dataclass
class ReadCSV(FileReader):
    def _do_load(self) -> pl.LazyFrame:
        return pl.scan_csv(self.config.file_path, **self.config.options)
