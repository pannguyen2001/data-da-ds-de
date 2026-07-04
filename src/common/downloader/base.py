import datetime
import time
import traceback
from abc import ABC, abstractmethod

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from src.common.constants import DownloadStatus
from src.common.logger import logger
from src.models.config.download_config import DownloadConfig
from src.models.metadata import MetaData
from src.models.result.download_result import DownloadResult


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Downloader(ABC):
    config: DownloadConfig

    def validate(self) -> None:
        """Validate arguments."""

        if not self.config.des_path:
            raise ValueError(
                f"[{self.__class__.__name__}] Need provide path for download."
            )

    @abstractmethod
    def download(self) -> None:
        """Download data from url."""

        pass

    # @logger_wrapper
    def execute(self) -> DownloadResult:
        """Execute dowload progress."""

        start_time = time.perf_counter()
        try:
            logger.info(
                f"[{self.__class__.__name__}] Downloading data:\n"
                f"- url: '{self.config.url}'\n"
                f"- destination: '{self.config.des_path}'"
            )

            self.validate()

            if self.config.skip_existing and self.config.des_path.exists():
                logger.info(
                    f"[{self.__class__.__name__}] Destination exists, skipping."
                )
                return DownloadResult(
                    source=self.config.url or self.config.id,
                    destination=self.config.des_path,
                    status=DownloadStatus.SKIPPED,
                    files_downloaded=[],
                    error=None,
                    duration_seconds=round(time.perf_counter() - start_time, 4),
                    metadata=MetaData(
                        end_at=datetime.datetime.now(datetime.timezone.utc)
                    ),
                )

            if self.config.dry_run:
                logger.info(
                    f"[{self.__class__.__name__}] DRY RUN: would download to {self.config.path}."
                )
                return DownloadResult(
                    source=self.config.url or self.config.id,
                    destination=self.config.des_path,
                    status=DownloadStatus.DRY_RUN,
                    files_downloaded=[],
                    error=None,
                    duration_seconds=round(time.perf_counter() - start_time, 4),
                    metadata=MetaData(
                        end_at=datetime.datetime.now(datetime.timezone.utc)
                    ),
                )

            self.download()

            if self.config.des_path.is_file():
                files = [self.config.des_path]

            elif self.config.des_path.is_dir():
                files = list(p for p in self.config.des_path.rglob("*") if p.is_file())

            else:
                files = []

            logger.success(f"[{self.__class__.__name__}] Complete downloading data.")

            return DownloadResult(
                source=self.config.url or self.config.id,
                destination=self.config.des_path,
                status=DownloadStatus.SUCCESS,
                files_downloaded=files,
                error=None,
                duration_seconds=round(time.perf_counter() - start_time, 4),
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )

        except Exception as e:
            logger.exception(f"[{self.__class__.__name__}] Download failed.")
            tb = "\n".join(traceback.TracebackException.from_exception(e).format())
            return DownloadResult(
                source=self.config.url or self.config.id,
                destination=self.config.des_path,
                status=DownloadStatus.FAILED,
                files_downloaded=[],
                error=tb,
                duration_seconds=round(time.perf_counter() - start_time, 4),
                metadata=MetaData(end_at=datetime.datetime.now(datetime.timezone.utc)),
            )
