from dataclasses import dataclass, field
from pathlib import Path

from src.common.config import (
    brozen_data_folder,
)
from src.common.constants import OperationStatus, ResolveFileType
from src.common.logger import logger
from src.io.connector.base import DatabaseConnector
from src.io.reader.base import FileReader
from src.io.storage.registry import _STORAGES
from src.models.config.storage_config import StorageConfig, StorageConfigBuilder
from src.models.result.db_connector_result import DbConnectorResult
from src.models.result.reader_result import ReaderResult
from src.models.result.storage_result import StorageResult
from src.pipeline.task.base import BaseTask


@dataclass
class StorageTask(BaseTask):
    always_run: bool = True
    detailed: dict = field(default_factory=dict)
    file_type: ResolveFileType | None = None
    storage_config: list[StorageConfig] = field(default_factory=list)
    des_folder_path: Path | None = brozen_data_folder

    def _collect_storage_reader_config(
        self, reader: FileReader
    ) -> StorageConfig | None:
        """Collect storage reader config."""

        result: ReaderResult = reader.load()
        logger.info(f"Reader result: {result.model_dump()}.")

        if result.status == OperationStatus.PASS:
            storage_config: StorageConfig = self.storage_config_builder.from_reader(
                result
            )

            self.detailed["collected_reader"].append(
                f"{str(result.source)} - {result.sheet if result.sheet is not None else ''}"
            )

            return storage_config

        else:
            logger.error(f"Reader error: {result.model_dump()}.")
            self.detailed["error_collected_reader"].append(str(result.source))
            raise RuntimeError(result.error)

    def _collect_storage_db_connector_config(
        self, dbconnector: DatabaseConnector
    ) -> StorageConfig | None:
        """Storage dbconnector."""

        dbconnecor_result: DbConnectorResult = dbconnector.run(dbconnector.config.query)

        if dbconnecor_result.status == OperationStatus.PASS:
            storage_config: StorageConfig = self.storage_config_builder.from_db(
                dbconnecor_result, dbconnector.config.connection_info
            )

            self.detailed["collected_dbconnector"].append(
                dbconnector.config.connection_info.database
                + "/"
                + dbconnector.config.connection_info.tb_or_collection
            )

            return storage_config
        else:
            logger.error(f"Dbconnector error: {dbconnecor_result.model_dump()}.")
            self.detailed["error_collected_dbconnector"].append(
                dbconnector.config.connection_info.database
                + "/"
                + dbconnector.config.connection_info.tb_or_collection
            )
            raise RuntimeError(dbconnecor_result.error)

    def _storage(self, storage_config: StorageConfig) -> None:
        """Storage data to folder."""

        storage_result: StorageResult = _STORAGES[self.file_type](storage_config).save()

        if storage_result.status == OperationStatus.FAIL:
            logger.error(f"Storage error: {storage_result.model_dump()}.")
            raise Exception(storage_result.error)

        logger.info(f"Storage result: {storage_result.model_dump()}.")

    def _execute(self) -> None:
        """
        Run storage task.
        1. Collect readers, connectors, downloader,... result.
        2. Build storage config.
        3. Storage data.
        """

        logger.info("Storage task start.")

        config: dict = self.context.setup.get("storage_config")
        self.file_type: ResolveFileType = config.get("file_type")
        self.detailed["collected_reader"] = []
        self.detailed["error_collected_reader"] = []
        self.detailed["collected_dbconnector"] = []
        self.detailed["error_collected_dbconnector"] = []

        self.storage_config_builder = StorageConfigBuilder(
            self.file_type, self.des_folder_path
        )

        for reader in self.context.readers:
            result = self._collect_storage_reader_config(reader)

            if result:
                self._storage(result)

        for dbconnector in self.context.dbconnectors:
            result = self._collect_storage_db_connector_config(dbconnector)

            if result:
                self._storage(result)
