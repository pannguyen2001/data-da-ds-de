import polars as pl
from pydantic.dataclasses import dataclass

from common.strategies.reader.base import FileReader


@dataclass
class ReadJson(FileReader):
    def _do_load(self) -> pl.DataFrame:
        return pl.read_json(self.config.file_path, **self.config.options)
