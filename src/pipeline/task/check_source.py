from dataclasses import field, dataclass

from src.io.connector.base import DatabaseConnector
from src.io.downloader.base import Downloader
from src.common.logger import logger
from src.io.reader.base import FileReader
from src.common.check_source_status import check_source_status
from src.models.result.source_status import SourceStatus
from src.pipeline.task.base import BaseTask


@dataclass
class CheckSourceTask(BaseTask):
    always_run: bool = True
    detailed: dict = field(default_factory=dict)

    def _check_file(self, reader: FileReader) -> bool:
        """Check file exist."""

        self.detailed["non_exist_file"] = []
        self.detailed["exist_file"] = []

        if not reader.config.file_path.exists():
            logger.error(f"File not found: {reader.config.file_path}. Remove this file from source config.")
            self.detailed["non_exist_file"].append(str(reader.config.file_path))
            return False

        self.detailed["exist_file"].append(str(reader.config.file_path))

        return True

    def _check_db(self):
        pass

    def _check_api(self):
        pass

    def _check_web(self):
        pass

    def _check_download(self, downloader: Downloader) -> bool:
        """Check source can download. Alert if source can not download."""

        self.detailed["unreachable_source"] = []
        self.detailed["reachable_source"] = []
        check_status_result: SourceStatus = check_source_status(
            downloader.config
        )

        logger.info(f"Download source status: {check_status_result.model_dump()}.")

        if not check_status_result.reachable:
            logger.error(f"Source can not download: {downloader.config}. Error: {check_status_result.error}. Remove this source from source config.")
            self.detailed["unreachable_source"].append(downloader.config.url)

        self.detailed["reachable_source"].append(downloader.config.url)

        return check_status_result.reachable

    def _execute(self) -> None:
        """Check and filter source can run. Alert if source can not run."""

        self.context.readers = [
            reader
            for reader in self.context.readers
            if self._check_file(reader)
        ]

        # for connector in self.dbconnectors:
        #     self._check_db(connector)

        self.context.downloaders = [
            downloader
            for downloader in self.context.downloaders
            if self._check_download(downloader)
        ]

        # for api in self.apis:
        #     self._check_api(api)

        # for web in self.webs:
        #     self._check_web(web)