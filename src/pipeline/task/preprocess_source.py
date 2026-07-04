from dataclasses import dataclass, field
from typing import Any

from python_calamine import CalamineWorkbook

from src.common.config import (
    brozen_data_folder,
)
from src.common.connector.base import DatabaseConnector
from src.common.constants import DownloadStatus, OperationStatus, ResolveFileType
from src.common.detect_file_type import detect_file_type
from src.common.downloader.base import Downloader
from src.common.logger import logger
from src.common.reader.base import FileReader
from src.common.reader.registry import _READERS
from src.models.config.file_config import FileConfig
from src.models.config.storage_config import StorageConfig
from src.models.result.download_result import DownloadResult
from src.models.result.reader_result import ReaderResult
from src.storage.storage import StorageData


@dataclass
class PreprocessSourceTask:
    config: dict

    data_list: list = field(default_factory=list)

    readers: list[FileReader] = field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = field(default_factory=list)
    downloaders: list[Downloader] = field(default_factory=list)

    def _preprocess_reader(self, reader: FileReader) -> None:
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
            if result.sheet is not None:
                des_file_name = f"{result.source.stem}/{result.sheet}.{self.file_type}"
            else:
                des_file_name = f"{result.source.stem}.{self.file_type}"

            storage_config: StorageConfig = StorageConfig(
                df=result.data,
                des_folder_path=brozen_data_folder,
                des_file_name=des_file_name,
                mode="w",
                options=None,
            )
            StorageData(config=storage_config, file_type=self.file_type).run()

        logger.info("Preprocess reader complete.")

    def _preprocess_dbconnector(self):
        """
        Preprocess dbconnector.
        1. Load dbconnector config.
        2. Read data from db.
        3. Save data as parquet to brozen.
        """

        pass

    def _preprocess_api(self):
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

    def _preprocess_web(self):
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

    def _preprocess_downloader(self, downloader: Downloader) -> None:
        """
        Preprocess downloader.
        1. Load downloader config.
        2. Check downloader status, get downloader can download, alert open db can not download.
        3. Convert result to file reader.
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

                if suffix == ResolveFileType.EXCEL:
                    sheet_names = CalamineWorkbook.from_path(
                        file_downloaded
                    ).sheet_names

                    for sheet in sheet_names:
                        options = {"sheet_name": sheet}

                        reader: FileReader = _READERS[suffix](
                            FileConfig(
                                file_path=file_downloaded,
                                file_type=ResolveFileType.EXCEL,
                                options=options,
                            )
                        )
                        self.readers.append(reader)
                else:
                    reader = _READERS[suffix](
                        FileConfig(file_path=file_downloaded, file_type=suffix)
                    )
                    self.readers.append(reader)

        logger.info("Preprocess downloader complete.")

    def run(self) -> Any:
        """Run preprocessing task."""

        self.file_type: ResolveFileType = self.config.get("file_type")

        # self._preprocess_dbconnector()

        # self._preprocess_api()

        # self._preprocess_web()

        if not self.downloaders:
            logger.info("No downloaders to preprocess.")
        else:
            for downloader in self.downloaders:
                self._preprocess_downloader(downloader)

        if not self.readers:
            logger.info("No readers to preprocess.")
        else:
            for reader in self.readers:
                self._preprocess_reader(reader)

    # Preprocessing
    # TODO
    # If need group data by file, ex: excel sheet A, A1, A2,.. having the same sheet name S1, S2,...; parquet file have the same file format: file_1.parquet, file_2.parquet,...; db table have the same table name: table_1, table_2,..., then group data by file, sheet, table name.
    # Staging: detect and group -> save as parquet -> transfer to raw
    # process mode: append, replace, onetime, incremental, just load update/delete/insert data, not load all or replace all. (SDC, CDC,...)
