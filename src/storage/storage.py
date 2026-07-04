from pydantic.dataclasses import dataclass

from src.common import logger
from src.common.constants import ResolveFileType
from src.common.storage.registry import _STORAGES
from src.models.config.storage_config import StorageConfig
from src.models.result.storage_result import StorageResult


@dataclass
class StorageData:
    config: StorageConfig
    file_type: ResolveFileType

    def run(self) -> None:
        try:
            storage_result: StorageResult = _STORAGES[self.file_type](
                self.config
            ).save()
            if storage_result:
                logger.info(f"Storage result: {storage_result.model_dump()}")

            logger.info("Storage data complete.")

        except Exception as e:
            logger.error(f"Error: {e}.")
            raise
