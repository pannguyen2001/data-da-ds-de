from dataclasses import dataclass, field
from typing import Any

import polars as pl

from src.common.logger import logger
from src.pipeline.task.base import BaseTask
from src.pipeline.task.build_io_config import BuildIOConfigTask
from src.pipeline.task.check_source import CheckSourceTask
from src.pipeline.task.preprocess_source import PreprocessSourceTask
from src.pipeline.task.storage import StorageTask
from src.pipeline.task.registry import _TASKS


@dataclass
class PrequisiteTaskCollection:
    failed_tasks: list[dict[str, Any]] | None = field(default_factory=list)
    result: list[str] | None = field(default_factory=list)

    _MAPPING_ORDER_TASKS: pl.DataFrame = field(default_factory=lambda: pl.DataFrame(
        {
            "task": list(_TASKS.keys()),
        },

    ).with_row_index("index"))

    def collect(self) -> list[str]:
        """Run task."""

        if not self.failed_tasks:
            logger.info("No failed task to collect prequisite tasks.")
            return self.result

        prequisite_task_list: set[str] = set
        for task in self.failed_tasks:
            prequisite_task_list = prequisite_task_list.union(set(task.get("prequisite_tasks", [])))

        if not prequisite_task_list:
            logger.info("No prequisite task.")
            return [task.get("task_name") for task in self.failed_tasks]

        # Order tasks to rerun
        self.failed_tasks = self._MAPPING_ORDER_TASKS.select(pl.col("task")).filter(pl.col("task").is_in(prequisite_task_list)).to_series().to_list()

        return self.failed_tasks
