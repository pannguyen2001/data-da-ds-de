from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

from src.io.connector.base import DatabaseConnector
from src.io.connector.registry import _DB_CONNECTORS
from src.common.constants import (
    DbEngine,
    DownloadSource,
    OperationStatus,
    ResolveFileType,
    SourceType,
)
from src.common.detect_file_type import detect_file_type
from src.io.downloader.base import Downloader
from src.io.downloader.registry import _DOWNLOADERS
from src.io.loader.registry import _LOADERS
from src.common.logger import logger
from src.io.reader.base import FileReader
from src.io.reader.registry import _READERS
from src.models.config.db_connector_config import DbConfig
from src.models.config.download_config import DownloadConfig
from src.models.config.file_config import FileConfig
from src.models.config.source_config import SourceConfig
from src.models.result.loader_result import LoaderResult
from src.pipeline.task.base import BaseTask


@dataclass
class BuildIOConfigTask(BaseTask):
    always_run: bool = True

    def _load_config(self, config: dict[str, Any]) -> Union[list, Any]:
        """
        Load source config.

        Args:
            config: source files configs.

        Returns:
            list: list of source configs. Example: {'data': [{'name': 'csv_file', 'source_type': 'file', 'config': {'file_path': 'configs/data_source.xlsx', 'file_type': 'excel', 'options': {'sheet_name': 'data_source', 'has_header': True}}}], 'source': Path('configs/source.yaml'), 'size_mb': 0.0011, 'status': <OperationStatus.PASS: 'pass'>, 'error': None, 'metadata': {'start_at': datetime.datetime(2026, 7, 6, 7, 41, 52, 636136), 'end_at': datetime.datetime(2026, 7, 6, 7, 41, 52, 636115, tzinfo=datetime.timezone.utc)}}.
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

    def _build_file_reader(self, file_config: dict) -> None:
        """
        Build file reader.

        Args:
            file_config (dict): file config to build reader. Example: {'name': 'csv_file', 'source_type': 'file', 'config': {'file_path': 'configs/data_source.xlsx', 'options': {'sheet_name': 'data_source', 'has_header': True}}}

        """

        suffix: ResolveFileType = detect_file_type(Path(file_config.get("file_path")))
        file_reader = FileConfig(**file_config)
        self.context.readers.append(_READERS[suffix](file_reader))

    def _build_db_connector(self, db_config: dict) -> None:
        """"""
        """Example: {'name': 'postgresql', 'source_type': 'database', 'config': {'engine': 'postgresql', 'connection_info': {'database': 'postgres', 'host': 'localhost', 'port': 5432, 'user': 'postgres', 'password': 'password'}, 'query': 'SELECT * FROM table', 'options': None}}"""

        engine: DbEngine = db_config.get("engine")
        db_connector = DbConfig(**db_config)
        self.context.dbconnectors.append(_DB_CONNECTORS[engine](db_connector))

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
        self.context.downloaders.append(_DOWNLOADERS[download_source_type](download_config))

    def _build_configs(self, loader_result: list[SourceConfig]) -> None:
        """Build configs."""

        logger.info("Build configs process.")

        for item in loader_result:
            if item is None:
                raise ValueError("Source config is None.")

            logger.info(f"Config: {item}.")
            source_type = item.get("source_type")
            data_config = item.get("config")

            match source_type:
                case SourceType.FILE:
                    self._build_file_reader(data_config)
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

        logger.info("Build configs complete.")

    def _execute(self):
        """Setup pipeline process."""

        logger.info("Setup pipeline.")

        config: list[dict] = self.context.setup.get("source_config", [])
        loader_result: list[SourceConfig] = []

        if not config:
            logger.warning("No config to setup.")
            self.checkpoint.mark_skipped()
            return self.context

        for item in config:
            logger.info(f"Config: {item}.")
            result = self._load_config(item)
            loader_result.extend(result)

        logger.info(loader_result)

        self._build_configs(loader_result)

        logger.info(f"Readers: {self.context.readers}.")
        logger.info(f"Connectors: {self.context.dbconnectors}.")
        logger.info(f"Downloaders: {self.context.downloaders}.")