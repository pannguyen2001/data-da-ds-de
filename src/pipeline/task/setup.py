from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.common.constants import SourceType, ResolveFileType, DbEngine
from src.common.loader.registry import _LOADERS
from src.common.detect_file_type import detect_file_type
from src.models.config.source_config import SourceConfig
from src.models.config.file_config import FileConfig
from src.models.config.db_connector_config import DbConfig
from src.common.reader.registry import _READERS
from src.common.connector.registry import _DB_CONNECTORS
from src.common.downloader.registry import _DOWNLOADERS
from src.common.constants import (
    DownloadSource,
    OperationStatus
)
from src.models.config.download_config import DownloadConfig
from src.common.logger import logger
from src.models.result.loader_result import LoaderResult

from src.common.downloader.base import Downloader
from src.common.reader.base import FileReader
from src.common.connector.base import DatabaseConnector



@dataclass
class SetupTask:

    config: list[dict] = field(default_factory=list)
    loader_result: list[LoaderResult] = field(default_factory=list)
    result: list[SourceConfig] = field(default_factory=list)

    readers: list[FileReader] = field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = field(default_factory=list)
    downloaders: list[Downloader] = field(default_factory=list)

    def _load_config(self, config: dict[str, Any]) -> LoaderResult:
        """Load source config."""

        logger.info("Load source config process.")

        suffix = detect_file_type(config.get("file_path"))
        config: FileConfig = FileConfig(**config)
        loader_result: LoaderResult = _LOADERS[suffix](config).load()

        logger.info(f"Load source config result: {loader_result.model_dump()}.")

        if loader_result.status != OperationStatus.PASS:
            raise Exception(loader_result.error)

        self.loader_result.extend(loader_result.data)

        logger.info("Load source config complete.")

    def _build_configs(self) -> None:
        """Build configs."""

        logger.info("Build configs process.")

        for item in self.loader_result:
            logger.info(f"Config: {item}.")
            source_type = item.get("source_type")
            config = item.get("config")

            match source_type:
                case SourceType.FILE:
                    """Example: {'name': 'csv_file', 'source_type': 'file', 'config': {'file_path': 'configs/data_source.xlsx', 'options': {'sheet_name': 'data_source', 'has_header': True}}}"""

                    suffix: ResolveFileType = detect_file_type(Path(config.get("file_path")))
                    file_reader = FileConfig(**config)
                    self.readers.append(_READERS[suffix](file_reader))

                case SourceType.DATABASE:
                    """Example: {'name': 'postgresql', 'source_type': 'database', 'config': {'engine': 'postgresql', 'connection_info': {'database': 'postgres', 'host': 'localhost', 'port': 5432, 'user': 'postgres', 'password': 'password'}, 'query': 'SELECT * FROM table', 'options': None}}"""

                    engine: DbEngine = config.get("engine")
                    db_connector = DbConfig(**config)
                    self.dbconnectors.append(_DB_CONNECTORS[engine](db_connector))

                case SourceType.API:
                    pass

                case SourceType.WEB:
                    pass

                case SourceType.OPEN_DB:
                    """Example: {'name': 'test_open_db', 'source_type': 'open_db', 'config': {'download_source_type': 'ggdrive', 'des_path': './data/0_staging', 'url': 'https://drive.google.com/drive/folders/folder_id', 'id': '', 'options': {'item_type': 'folder', 'quiet': False}}}"""

                    download_source_type: DownloadSource = config.get("download_source_type")
                    download_config = DownloadConfig(**config)
                    self.downloaders.append(_DOWNLOADERS[download_source_type](download_config))

                case _:
                    raise ValueError(f"[{self.__class__.__name__}] Invalid source type: {source_type}.")

        logger.info(f"Connectors: {self.dbconnectors}.")
        logger.info(f"Readers: {self.readers}.")
        logger.info(f"Downloaders: {self.downloaders}.")
        logger.info("Build configs complete.")

    def run(self) -> tuple[list[FileReader], list[DatabaseConnector], list[Downloader]]:
        """Setup pipeline process."""

        logger.info("Setup pipeline.")

        for item in self.config:
            logger.info(f"Config: {item}.")
            self._load_config(item)

        self._build_configs()

        # Load last checkpoint and status to know which need run, which can skip

        logger.info(f"Readers: {self.readers}.")
        logger.info(f"Connectors: {self.dbconnectors}.")
        logger.info(f"Downloaders: {self.downloaders}.")
        logger.info("Setup pipeline complete.")

        return (
            self.readers,
            self.dbconnectors,
            self.downloaders
        )
