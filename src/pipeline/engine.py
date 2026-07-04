from pydantic.dataclasses import dataclass
from pathlib import Path
from pydantic import Field
from typing import Any
from python_calamine import CalamineWorkbook

import polars as pl

from src.common.constants import SourceType, ResolveFileType, DbEngine

from src.common.loader.registry import _LOADERS
from src.common.detect_file_type import detect_file_type
from src.models.config.source_config import SourceConfig
from src.models.config.file_config import FileConfig
from src.models.config.api_config import ApiConfig
from src.models.config.db_connector_config import DbConfig

from src.common.reader.registry import _READERS
from src.common.reader.base import FileReader
from src.common.connector.registry import _DB_CONNECTORS
from src.common.connector.base import DatabaseConnector
from src.common.downloader.registry import _DOWNLOADERS
from src.common.downloader.base import Downloader

from src.common.constants import (
    DownloadSource,
    DownloadStatus,
    OperationStatus
)

from src.models.config.download_config import DownloadConfig

from src.common.logger import logger
from src.common.config import (
    staging_data_folder,
    brozen_data_folder,
    silver_data_folder,
    golden_data_folder,
    test_data_folder,
)
from src.common.storage.registry import _STORAGES
from src.models.result.download_result import DownloadResult
from src.models.result.reader_result import ReaderResult
from src.models.result.storage_result import StorageResult
from src.models.result.loader_result import LoaderResult
from src.pipeline.task.source import SourceTask
from src.pipeline.task.setup import SetupTask

@dataclass
class PipelineEngine:
    """
    Pipeline.run()
        ↓
        load source_config.yaml
        ↓
        parse yaml
        ↓
        build SourceConfig list
        ↓
        for source in sources
        if file:
            create reader
            reader.read() from staging

        if database:
            create connector
            connector.read()
            save() to staging
        if api:
            check api status, download or not
            call api
            save() to staging
        if web:
            web scraping
            save() to staging

        transfer file type()
        storage() to raw

        each file need:
            validate()
            transform()
            save()
            checkpoint()
            report()
            orchestration()
            mornitoring()
        -> batch process
        Future:
            multi threads
            multiple processes
            ELT pipeline
            conect cloud: Databrick, GCP, AWS
            optimize

    """

    setup: dict[str, Any] = Field(default_factory=dict)
    source_configs: list[SourceConfig] = Field(default_factory=list)

    readers: list[FileReader] = Field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = Field(default_factory=list)
    downloaders: list[Downloader] = Field(default_factory=list)

    def storage_data(self, data: pl.LazyFrame, folder_path: Path, file_name: str) -> None:
        """
        Storage data.
        1. Load storage config.
        2. Save data to storage.
        """

        logger.info("Storage data process.")

        if not folder_path:
            raise ValueError("Folder path is required.")

        if not folder_path.exists():
            logger.warning(
                "File not found: {str(folder_path)}. Create new."
            )
            folder_path.mkdir(parents=True, exist_ok=True)

        if not folder_path.is_dir():
            raise ValueError(
                "Invalid folder path: {str(folder_path)}."
            )

        if not file_name:
            raise ValueError("File name is required.")

        file_type: ResolveFileType = self.setup["storage_file_type"]
        des_file_path = folder_path / f"{file_name}.{file_type.value}"
        logger.info(f"Des file path: {des_file_path}")

        storage_result: StorageResult = _STORAGES[ResolveFileType.PARQUET](df=data, des_file_path=des_file_path).save()
        if storage_result:
            logger.info(f"Storage result: {storage_result.model_dump()}")

        logger.info("Storage data complete.")

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


    @logger.catch
    def run(self):
        """
        Run pipeline.
        1. Setup pipeline.
        2. Preprocess readers.
        3. Preprocess dbconnectors.
        4. Preprocess apis.
        5. Preprocess web.
        6. Preprocess downloader.
        """

        # Setup
        source_config: list[dict, Any] = self.setup.get("source_config", [])
        self.readers, self.dbconnectors, self.downloaders = SetupTask(source_config).run()

        # Preprocessing
        # TODO
        # If need group data by file, ex: excel sheet A, A1, A2,.. having the same sheet name S1, S2,...; parquet file have the same file format: file_1.parquet, file_2.parquet,...; db table have the same table name: table_1, table_2,..., then group data by file, sheet, table name.
        # Staging: detect and group -> save as parquet -> transfer to raw
        # process mode: append, replace, onetime, incremental, just load update/delete/insert data, not load all or replace all. (SDC, CDC,...)
        # if not self.readers:
        #     logger.info("No readers to preprocess.")
        # else:
        #     for reader in self.readers:
        #         self.preprocess_reader(reader)

        # self.preprocess_dbconnector()

        # self.preprocess_api()

        # self.preprocess_web()

        # if not self.downloaders:
        #     logger.info("No downloaders to preprocess.")
        # else:
        #     for downloader in self.downloaders:
        #         self.preprocess_downloader(downloader)

        # Validate

        # Transform

        # .....

        # TODO: Add checkpoint
        # ckecpoint, status, log, alert, mornitoring, orchestration, report for each step
        # check api status -> download or  not
        # file -> transfer to sql or parquet -> save to raw

"""
2026-July-03

setup
    │
    ▼
main.py
    │
    ▼
PipelineEngine
    │
    ├───────────────┐
    ▼               ▼
SetupTask      SourceTask
                    │
     ┌──────────────┼─────────────────────┐
     ▼              ▼                     ▼
 FileReader     DbConnector        Downloader
     │              │                   │
     └──────────────┴───────────────────┘
                    │
             ReaderResult
                    │
                    ▼
          Discovery / Grouping
                    │
                    ▼
            StorageManager
                    │
                    ▼
           CheckpointManager
                    │
                    ▼
          ValidationManager
                    │
                    ▼
         TransformationEngine
                    │
                    ▼
             Silver Storage
                    │
                    ▼
              Gold Storage
                    │
                    ▼
             Report Manager
                    │
                    ▼
            Alert / Monitoring
"""