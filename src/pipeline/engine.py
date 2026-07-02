from pydantic.dataclasses import dataclass
from pathlib import Path
from pydantic import Field
from typing import Any

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

from src.common.logger import logger
from src.common.config import (
    staging_data_folder,
    brozen_data_folder,
    silver_data_folder,
    golden_data_folder,
    test_data_folder,
)
from src.common.storage.registry import _STORAGES


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

    def load_source_config(self, source_config_path: Path, options: dict) -> None:
        suffix = detect_file_type(source_config_path)
        self.source_configs = _LOADERS[suffix](source_config_path, options).load()

    def build_configs(self) -> None:
        for item in self.source_configs:
            logger.info(f"Config: {item}.")
            source_type = item.get("source_type")
            config = item.get("config")

            match source_type:
                case SourceType.FILE:
                    suffix: ResolveFileType = detect_file_type(Path(config.get("file_path")))
                    file_reader = FileConfig(**config)
                    self.readers.append(_READERS[suffix](file_reader))
                case SourceType.DATABASE:
                    engine: DbEngine = config.get("engine")
                    db_connector = DbConfig(**config)
                    self.dbconnectors.append(_DB_CONNECTORS[engine](db_connector))
                case SourceType.API:
                    pass
                case SourceType.WEB:
                    pass
                case _:
                    raise ValueError(f"[{self.__class__.__name__}] Invalid source type: {source_type}.")

    def transfer_file_type(self):
        pass

    def process_readers(self):
        pass

    def process_dbconnectors(self):
        pass

    def process_apis(self):
        pass

    def run(self):
        # Setup
        self.load_source_config(source_config_path=self.setup["source_config_path"], options=self.setup["options"])
        self.build_configs()
        logger.info(self.readers)

        # Preprocessing
        # For file, if not parquet, load to parquet and save to raw
        for reader in self.readers:
            result = reader.load()
            logger.info(result.model_dump())
            des_file_path = Path(
                f"{brozen_data_folder}/{result.source.stem}.parquet"
            )
            logger.info(f"Des file path: {des_file_path}")
            storage_result = _STORAGES[ResolveFileType.PARQUET](df=result.data, des_file_path=des_file_path).save()
            logger.info(storage_result.model_dump())

        # If API, check api status, can download or not, call api and save to staging. If not parquet -> load to parquet and save to staging

        # If db, read from db and load to parquet and save to staging

        # If web, check web status -> crawl or not -> crawl and save to staging -> if not parquet -> load to parquet and save to staging


        # Validate

        # Transform

        # .....

        # ckecpoint, status, log, alert, mornitoring, orchestration, report for each step
        # check api status -> download or  not
        # file -> transfer to sql or parquet -> save to raw