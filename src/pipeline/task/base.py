from abc import ABC, abstractmethod
from typing import Any

from dataclasses import dataclass, field

from src.common.logger import logger
from src.checkpoint.manager import Checkpoint
from src.pipeline.context import PipelineContext

@dataclass
class BaseTask(ABC):

    # config: list[dict] | None = None
    # checkpoint: Checkpoint = field(default_factory=Checkpoint)
    # result: Any | None = None

    context: PipelineContext = field(default_factory=PipelineContext)
    checkpoint: Checkpoint = field(default_factory=Checkpoint)
    always_run: bool = False
    detailed: Any | None = None

    @abstractmethod
    def _execute(self):
        """Execute the task."""

        raise NotImplementedError

    def run(self) -> Checkpoint:
        """Run the task."""

        logger.info(f"Execute task {self.__class__.__name__}.")
        self.checkpoint = Checkpoint(task_name=self.__class__.__name__)

        try:
            self._execute()

        except Exception as e:
            logger.error(f"Error running task {self.__class__.__name__}.")
            self.checkpoint.mark_failed(error=e)

        else:
            logger.info(f"Task {self.__class__.__name__} complete.")
            self.checkpoint.mark_passed()
            self.checkpoint.get_detailed(detailed=self.detailed)

        return self.checkpoint
