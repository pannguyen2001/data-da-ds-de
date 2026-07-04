import os

import polars as pl
from huggingface_hub import hf_hub_download
from pydantic.dataclasses import dataclass

from src.common.downloader.base import Downloader


@dataclass
class HuggingFaceDownloader(Downloader):
    def validate(self) -> None:
        super().validate()

        if not self.config.id:
            raise ValueError("id is required")

        if not self.options.get("file_name"):
            raise ValueError(
                "file_name is required in kwargs for HuggingFaceDownloader"
            )

    def _save_to_parquet(self, file_path: str) -> None:
        pl.scan_parquet(file_path).sink_parquet(str(self.config.des_path))
        if os.path.exists(file_path):
            os.remove(file_path)

    def _download(self) -> None:
        file_path = hf_hub_download(
            repo_id=self.config.id,
            filename=self.options.get("file_name"),
            repo_type="dataset",
        )

        self._save_to_parquet(file_path)
