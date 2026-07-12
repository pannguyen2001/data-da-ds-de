from kaggle.api.kaggle_api_extended import KaggleApi
from pydantic.dataclasses import dataclass

from src.io.downloader.base import Downloader


@dataclass
class KaggleDownloader(Downloader):
    _api: KaggleApi | None = None

    def _validate(self) -> None:
        super().validate()

        if not self.config.id:
            raise ValueError(
                f"[{self.__class__.__name__}] Need provide id for kaggle dataset."
            )

    @classmethod
    def _get_api(cls) -> KaggleApi:
        if cls._api is None:
            api = KaggleApi()
            api.authenticate()
            cls._api = api
        return cls._api

    def _download(self) -> None:
        self._get_api().dataset_download_files(
            self.config.id, path=self.config.des_path, **self.options
        )
