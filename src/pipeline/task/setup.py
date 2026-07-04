from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

from src.common.connector.base import DatabaseConnector
from src.common.connector.registry import _DB_CONNECTORS
from src.common.constants import (
    DbEngine,
    DownloadSource,
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
from src.models.config.db_connector_config import DbConfig
from src.models.config.download_config import DownloadConfig
from src.models.config.file_config import FileConfig
from src.models.config.source_config import SourceConfig
from src.models.result.loader_result import LoaderResult


@dataclass
class SetupTask:
    config: list[dict] = field(default_factory=list)
    loader_result: list[SourceConfig] = field(default_factory=list)

    readers: list[FileReader] = field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = field(default_factory=list)
    downloaders: list[Downloader] = field(default_factory=list)

    def _load_config(self, config: dict[str, Any]) -> Union[list, Any]:
        """
        Load source config.

        Args:
            config: source files configs.

        Returns:
            list[SourceConfig]
        """

        logger.info("Load source config process.")

        if config is None:
            raise ValueError("config is None.")

        if not config:
            logger.warning("config is empty.")
            return []

        suffix = detect_file_type(Path(config.get("file_path")))
        file_config: FileConfig = FileConfig(**config)
        loader_result: LoaderResult = _LOADERS[suffix](file_config).load()

        logger.info(f"Load source config result: {loader_result.model_dump()}.")

        if loader_result.status != OperationStatus.PASS:
            raise Exception(loader_result.error)

        logger.info("Load source config complete.")

        return loader_result.data

    def _buidld_file_reader(self, file_config: dict) -> None:
        """
        Build file reader.

        Args:
            file_config (dict): file config to build reader. Example: {'name': 'csv_file', 'source_type': 'file', 'config': {'file_path': 'configs/data_source.xlsx', 'options': {'sheet_name': 'data_source', 'has_header': True}}}

        """

        suffix: ResolveFileType = detect_file_type(Path(file_config.get("file_path")))
        file_reader = FileConfig(**file_config)
        self.readers.append(_READERS[suffix](file_reader))

    def _build_db_connector(self, db_config: dict) -> None:
        """"""
        """Example: {'name': 'postgresql', 'source_type': 'database', 'config': {'engine': 'postgresql', 'connection_info': {'database': 'postgres', 'host': 'localhost', 'port': 5432, 'user': 'postgres', 'password': 'password'}, 'query': 'SELECT * FROM table', 'options': None}}"""

        engine: DbEngine = db_config.get("engine")
        db_connector = DbConfig(**db_config)
        self.dbconnectors.append(_DB_CONNECTORS[engine](db_connector))

    def _build_api_connector(self, api_config: dict) -> None:
        """"""

    def _build_web_crawler(self, web_config: dict) -> None:
        """"""

    def _build_opendb_downloader(self, opendb_config: dict) -> None:
        """
        Build opendb downloader.

        Args:
            opendb_config (dict): opendb config. Example: {'name': 'test_OPENDB', 'source_type': 'OPENDB', 'config': {'download_source_type': 'ggdrive', 'des_path': './data/0_staging', 'url': 'https://drive.google.com/drive/folders/folder_id', 'id': '', 'options': {'item_type': 'folder', 'quiet': False}}}
        """

        download_source_type: DownloadSource = opendb_config.get("download_source_type")
        download_config = DownloadConfig(**opendb_config)
        self.downloaders.append(_DOWNLOADERS[download_source_type](download_config))

    def _build_configs(self) -> None:
        """Build configs."""

        logger.info("Build configs process.")

        for item in self.loader_result:
            if item is None:
                raise ValueError("Source config is None.")

            logger.info(f"Config: {item}.")
            source_type = item.get("source_type")
            data_config = item.get("config")

            match source_type:
                case SourceType.FILE:
                    self._buidld_file_reader(data_config)
                case SourceType.DATABASE:
                    self._build_db_connector(data_config)
                case SourceType.API:
                    self._build_api_connector(data_config)
                case SourceType.WEB:
                    self._build_web_crawler(data_config)
                case SourceType.OPENDB:
                    self._build_opendb_downloader(data_config)
                case _:
                    raise ValueError(
                        f"[{self.__class__.__name__}] Invalid source type: {source_type}."
                    )

        logger.info(f"Connectors: {self.dbconnectors}.")
        logger.info(f"Readers: {self.readers}.")
        logger.info(f"Downloaders: {self.downloaders}.")
        logger.info("Build configs complete.")

    def run(self) -> tuple[list[FileReader], list[DatabaseConnector], list[Downloader]]:
        """Setup pipeline process."""

        logger.info("Setup pipeline.")

        if not self.config:
            logger.warning("No config to setup.")
            return ([], [], [])

        for item in self.config:
            logger.info(f"Config: {item}.")
            result = self._load_config(item)
            self.loader_result.extend(result)

        logger.info(self.loader_result)

        self._build_configs()

        # Load last checkpoint and status to know which need run, which can skip

        logger.info(f"Readers: {self.readers}.")
        logger.info(f"Connectors: {self.dbconnectors}.")
        logger.info(f"Downloaders: {self.downloaders}.")
        logger.info("Setup pipeline complete.")

        return (self.readers, self.dbconnectors, self.downloaders)
