from dataclasses import dataclass, field
from typing import Any

from src.common.logger import logger
from src.common.constants import OperationStatus
from src.io.loader.registry import _LOADERS


@dataclass
class FailedTaskCollection:
    config: dict[str, Any]

    last_checkpoint_result: dict[str, Any] | None = None
    result: list[str] = field(default_factory=list)

    def collect(self) -> list[str] | None:
        """Collect failed task from last checkpoint."""

        if self.config is None:
            logger.info("No last checkpoint config. Run pipleine from start.")
            return self.result

        self.last_checkpoint_result = _LOADERS[self.config.get("file_type")](self.config).load()
        logger.info(f"Last checkpoint: {self.last_checkpoint_result}")

        if self.last_checkpoint_result.status != OperationStatus.PASS:
            raise Exception(self.last_checkpoint_result.error)

        if not self.last_checkpoint_result.data:
            logger.info("No last checkpoint data. Run pipleine from start.") # will run from start
            return self.result

        self.result = [failed_task for failed_task in self.last_checkpoint_result.data.get("results", []) if failed_task.get("status") == OperationStatus.FAIL]

        return self.result