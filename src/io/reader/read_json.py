import polars as pl
from pydantic.dataclasses import dataclass

from src.io.reader.base import FileReader


@dataclass
class JsonReader(FileReader):
    def _do_load(self) -> pl.LazyFrame:
        return pl.read_json(self.config.file_path, **self.config.options).lazy()
