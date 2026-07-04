from pathlib import Path
from typing import Any

import polars as pl
from pydantic import Field
from pydantic.dataclasses import dataclass
from python_calamine import CalamineWorkbook

from src.common.config import (
    brozen_data_folder,
    golden_data_folder,
    silver_data_folder,
    staging_data_folder,
    test_data_folder,
)
from src.common.connector.base import DatabaseConnector
from src.common.connector.registry import _DB_CONNECTORS
from src.common.constants import (
    DbEngine,
    DownloadSource,
    DownloadStatus,
    OperationStatus,
    ResolveFileType,
    SourceType,
)
from src.common.detect_file_type import detect_file_type
from src.common.downloader.base import Downloader
from src.common.downloader.registry import _DOWNLOADERS
from src.common.loader.registry import _LOADERS
from src.common.logger import logger
from src.common.reader.base import FileReader
from src.common.reader.registry import _READERS
from src.common.storage.registry import _STORAGES
from src.models.config.api_config import ApiConfig
from src.models.config.db_connector_config import DbConfig
from src.models.config.download_config import DownloadConfig
from src.models.config.file_config import FileConfig
from src.models.config.source_config import SourceConfig
from src.models.result.download_result import DownloadResult
from src.models.result.loader_result import LoaderResult
from src.models.result.reader_result import ReaderResult
from src.models.result.storage_result import StorageResult

# from src.pipeline.task.source import SourceTask
from src.pipeline.task.preprocess_source import PreprocessSourceTask
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

    readers: list[FileReader] = Field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = Field(default_factory=list)
    downloaders: list[Downloader] = Field(default_factory=list)

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
        source_config: list[dict] = self.setup.get("source_config", [])
        storage_config: dict = self.setup.get("storage_config", [])

        self.readers, self.dbconnectors, self.downloaders = SetupTask(
            source_config
        ).run()

        # Preprocessing
        PreprocessSourceTask(
            config=storage_config,
            readers=self.readers,
            dbconnectors=self.dbconnectors,
            downloaders=self.downloaders,
        ).run()

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
