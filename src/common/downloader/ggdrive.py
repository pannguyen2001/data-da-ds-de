from pydantic.dataclasses import dataclass

import gdown

from src.common.downloader.base import Downloader


# @dataclass(slots=True)
class GoogleDriveDownloader(Downloader):

    def validate(self) -> None:
        super().validate()

        if self.config.options.item_type not in ("file", "folder"):
            raise ValueError(f"[{self.__class__.__name__}] type must be 'file' or 'folder'")

        if self.config.options.item_type == "folder":
            if not self.config.url and not self.config.id:
                raise ValueError(f"[{self.__class__.__name__}] Need provide url or id for folder download.")
        else:
            if not self.config.url:
                raise ValueError(f"[{self.__class__.__name__}] Need provide url for file download.")

    def _download_folder(self) -> None:
        if self.config.url:
            gdown.download_folder(
                url=self.config.url,
                output=str(self.config.des_path),
                **self.config.options.model_dump(exclude_none=True),
            )
            return

        if self.config.id:
            gdown.download_folder(
                id=self.config.id,
                output=str(self.config.des_path),
                **self.config.options.model_dump(exclude_none=True),
            )
            return

    def _download_file(self) -> None:
        gdown.download(
            url=self.config.url,
            output=str(self.config.des_path),
            **self.config.options.model_dump(exclude_none=True)
        )

    def download(self) -> None:
        item_type = self.config.options.item_type
        del self.config.options.item_type

        if item_type == "folder":
            self._download_folder()
        else:
            self._download_file()

        # TODO: if can not download without auth, use auth as fallback