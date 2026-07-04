from dataclasses import dataclass, field
from python_calamine import CalamineWorkbook


from src.common.constants import ResolveFileType

from src.common.detect_file_type import detect_file_type
from src.models.config.file_config import FileConfig

from src.common.reader.registry import _READERS
from src.common.reader.base import FileReader
from src.common.connector.base import DatabaseConnector
from src.common.downloader.base import Downloader

from src.common.constants import (
    DownloadStatus,
    OperationStatus
)

from src.common.logger import logger
from src.common.config import (
    brozen_data_folder,
)
from src.models.result.download_result import DownloadResult
from src.models.result.reader_result import ReaderResult


@dataclass
class PreprocessSourceTask:

    readers: list[FileReader] = field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = field(default_factory=list)
    downloaders: list[Downloader] = field(default_factory=list)

    def preprocess_reader(self, reader: FileReader) -> None:
        """
        Preprocess reader.
        1. Load reader config.
        2. Read data from file.
        3. Save data as parquet to brozen.
        # TODO:
            - Read save mode: a: append, w: replace and write, o: onetime only load, i: incremental load,  just load update/delete/insert data, not load all or replace all. (SDC, CDC,...)
            - if o mode: check if exist and not empty: return None, else save data.
        """

        logger.info("Preprocess reader process.")

        result: ReaderResult = reader.load()
        logger.info(f"Reader result: {result.model_dump()}.")

        if result.status == OperationStatus.PASS:
            self.storage_data(
                data=result.data,
                folder_path=brozen_data_folder,
                file_name=result.source.stem,
            )

        logger.info("Preprocess reader complete.")

    def preprocess_dbconnector(self):
        """
        Preprocess dbconnector.
        1. Load dbconnector config.
        2. Read data from db.
        3. Save data as parquet to brozen.
        """

        pass

    def preprocess_api(self):
        """
        Preprocess api.
        1. Load api config.
        2. Check API status, get API can download, alert API can not download.
        2. Read data from API.
        3. Save data as parquet to staging.
        4. If data is not parquet, load data to parquet.
        5. Save to staging.
        """

        pass

    def preprocess_web(self):
        """
        Preprocess web.
        1. Load web config.
        2. Check web status, get web can crawl, alert web can not crawl.
        2. Read data from web.
        3. Save data as parquet to staging.
        4. If data is not parquet, load data to parquet.
        5. Save to staging.
        """

        pass

    def preprocess_downloader(self, downloader: Downloader)-> None:
        """
        Preprocess downloader.
        1. Load downloader config.
        2. Check downloader status, get downloader can download, alert open db can not download.
        2. Read data from downloader.
        3. Save data as parquet to staging.
        4. If data is not parquet, load data to parquet.
        5. Save to staging.
        """

        logger.info("Preprocess downloader process.")

        download_result: DownloadResult = downloader.execute()
        logger.info(f"Downloader result: {download_result.model_dump()}.")

        if download_result.status == DownloadStatus.SUCCESS:
            for file_downloaded in download_result.files_downloaded:
                try:
                    suffix: ResolveFileType = detect_file_type(file_downloaded)
                except Exception as e:
                    logger.error(e)
                    continue

                readers: list[FileReader] = []

                if suffix == ResolveFileType.EXCEL:
                    sheet_names = CalamineWorkbook.from_path(file_downloaded).sheet_names

                    for sheet in sheet_names:
                        options = {"sheet_name": sheet}
                        reader = _READERS[suffix](FileConfig(file_path=file_downloaded, options=options))

                        result: ReaderResult = reader.load()
                        logger.info(f"Reader result: {result.model_dump()}.")

                        if result.status == OperationStatus.PASS:
                            self.storage_data(
                                data=result.data,
                                folder_path=brozen_data_folder,
                                file_name=f"{result.source.stem}/{sheet}",
                            )

                else:
                    reader = [_READERS[suffix](FileConfig(file_path=file_downloaded))]
                    self.preprocess_reader(readers)

        logger.info("Preprocess downloader complete.")
