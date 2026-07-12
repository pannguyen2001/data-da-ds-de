from dataclasses import field, dataclass

from src.common.config import (
    brozen_data_folder,
)
from src.common.constants import OperationStatus
from src.common.logger import logger
from src.io.reader.base import FileReader
from src.models.result.reader_result import ReaderResult
from src.io.storage.registry import _STORAGES
from src.models.result.storage_result import StorageResult
from src.models.config.storage_config import StorageConfig
from src.common.constants import ResolveFileType
from src.io.downloader.base import Downloader
from src.io.connector.base import DatabaseConnector
from src.models.result.db_connector_result import DbConnectorResult
from src.pipeline.task.base import BaseTask


@dataclass
class StorageTask(BaseTask):
    always_run: bool = True
    detailed: dict = field(default_factory=dict)
    file_type: ResolveFileType | None = None
    storage_config: list[StorageConfig] = field(default_factory=list)

    def _collect_storage_reader_config(self, reader: FileReader) -> StorageConfig | None:
        """Collect storage reader config."""

        result: ReaderResult = reader.load()
        logger.info(f"Reader result: {result.model_dump()}.")

        if result.status == OperationStatus.PASS:
            if result.sheet is not None:
                des_file_name = f"{result.source.stem}/{result.sheet}.{self.file_type}"
            else:
                folder_name = result.source.parent.name or "unknown"
                des_file_name = f"{folder_name}/{result.source.stem}.{self.file_type}"

            storage_config: StorageConfig = StorageConfig(
                df=result.data,
                des_folder_path=brozen_data_folder,
                des_file_name=des_file_name,
                mode="w",
                options=None,
            )
            self.detailed["collected_reader"].append(str(des_file_name))

            return storage_config
        else:
            logger.error(f"Reader error: {result.model_dump()}.")
            self.detailed["error_collected_reader"].append(str(result.source))
            raise Exception(result.error)

    def _collect_storage_db_connector_config(self, dbconnector: DatabaseConnector) -> StorageConfig | None:
        """Storage dbconnector."""

        dbconnecor_result: DbConnectorResult = dbconnector.run(dbconnector.config.query)

        if dbconnecor_result.status == OperationStatus.PASS:
            connection_info = dbconnector.config.connection_info
            des_file_name = f"{connection_info.database}/{connection_info.tb_or_collection}.{self.file_type}"
            storage_config: StorageConfig = StorageConfig(
                df=dbconnecor_result.data,
                des_folder_path=brozen_data_folder,
                des_file_name=des_file_name,
                mode="w",
                options=None,
            )

            self.detailed["collected_dbconnector"].append(dbconnector.config.connection_info.database + "/" + dbconnector.config.connection_info.tb_or_collection)

            return storage_config
        else:
            logger.error(f"Dbconnector error: {dbconnecor_result.model_dump()}.")
            self.detailed["error_collected_dbconnector"].append(dbconnector.config.connection_info.database + "/" + dbconnector.config.connection_info.tb_or_collection)
            raise Exception(dbconnecor_result.error)

    def _storage(self, storage_config: StorageConfig) -> None:
        """Storage data to folder."""

        storage_result: StorageResult = _STORAGES[self.file_type](
            storage_config
        ).save()

        if storage_result.status == OperationStatus.FAIL:
            logger.error(f"Storage error: {storage_result.model_dump()}.")
            raise Exception(storage_result.error)

        logger.info(f"Storage result: {storage_result.model_dump()}.")

    def _execute(self) -> None:
        """
        Run storage task.
        1. Collect reader, connectore, downloaders,... result.
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

        for reader in self.context.readers:
            result = self._collect_storage_reader_config(reader)

            if result:
                self.storage_config.append(result)

        for dbconnector in self.context.dbconnectors:
            result = self._collect_storage_db_connector_config(dbconnector)

            if result:
                self.storage_config.append(result)

        for storage_config in self.storage_config:
            self._storage(storage_config)