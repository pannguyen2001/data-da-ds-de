from pydantic.dataclasses import dataclass

from src.io.storage.base import Storage


@dataclass
class ParquetStorage(Storage):
    def _do_save(self) -> None:
        return self.config.df.sink_parquet(self.des_file_path, **self.config.options)
