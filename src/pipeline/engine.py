from typing import Any

from dataclasses import dataclass, field

from src.common.logger import logger
from src.io.connector.base import DatabaseConnector
from src.io.downloader.base import Downloader
from src.io.reader.base import FileReader
from src.pipeline.task.build_io_config import BuildIOConfigTask
from src.pipeline.task.check_source import CheckSourceTask
from src.pipeline.task.preprocess_source import PreprocessSourceTask
from src.pipeline.task.storage import StorageTask
from src.checkpoint.manager import CheckpointManager
from src.io.loader.registry import _LOADERS
from src.common.constants import OperationStatus
from src.pipeline.context import PipelineContext
from src.checkpoint.manager import Checkpoint


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

    setup: dict[str, Any] = field(default_factory=dict)
    context: PipelineContext = field(default_factory=PipelineContext)

    @logger.catch
    def run(self):
        """
        Run pipeline.
        1. Setup pipeline.
        2. Check source status.
        3. Preprocess source.
        4. Storage to raw.
        """

        # ==============================
        # Config
        # ==============================
        self.context.setup = self.setup
        previous_checkpoint: list[Checkpoint] = CheckpointManager(config=self.context.setup.get("checkpoint")).load_checkpoint()
        logger.info(f"Previous checkpoint: {previous_checkpoint}.")

        failed_task: list[str] = [task.task_name for task in previous_checkpoint if task.status == OperationStatus.FAIL]
        logger.info(f"Previous failed task: {failed_task}.")

        TASKS = [
            BuildIOConfigTask(context=self.context),
            CheckSourceTask(context=self.context),
            PreprocessSourceTask(context=self.context),
            StorageTask(context=self.context)
        ]

        # ==============================
        # Process
        # ==============================
        if not previous_checkpoint:
            for task in TASKS:
                task_checkpoint = task.run()
                self.context.checkpoint.add_checkpoint(task_checkpoint)
                continue
        else:
            resume = False
            for task in TASKS:
                if task.always_run:
                    task_checkpoint = task.run()
                    self.context.checkpoint.add_checkpoint(task_checkpoint)
                    continue

                if resume:
                    task_checkpoint = task.run()
                    self.context.checkpoint.add_checkpoint(task_checkpoint)
                    continue

                is_passed = task.__class__.__name__ not in failed_task
                if is_passed:
                    logger.info(f"Skip task {task.__class__.__name__}.")
                    self.context.checkpoint.add_checkpoint(Checkpoint(task_name=task.__class__.__name__, status=OperationStatus.SKIP))
                    continue

                resume = True
                logger.info(f"Resume task {task.__class__.__name__}.")
                task_checkpoint = task.run()
                self.context.checkpoint.add_checkpoint(task_checkpoint)


        # # Validate

        # # Transform

        # # .....

        # ==============================
        # Conclusion
        # ==============================
        # Save check point
        self.context.checkpoint.save_checkpoint()

        # TODO: Add checkpoint
        # ckecpoint, status, log, alert, mornitoring, orchestration, report for each step


"""
2026-July-03

setup
    │
    ▼
main.py
    │
    ▼
PipelineEngine
    │
    ├───────────────┐
    ▼               ▼
SetupTask      SourceTask
                    │
     ┌──────────────┼─────────────────────┐
     ▼              ▼                     ▼
 FileReader     DbConnector        Downloader
     │              │                   │
     └──────────────┴───────────────────┘
                    │
             ReaderResult
                    │
                    ▼
          Discovery / Grouping
                    │
                    ▼
            StorageManager
                    │
                    ▼
           CheckpointManager
                    │
                    ▼
          ValidationManager
                    │
                    ▼
         TransformationEngine
                    │
                    ▼
             Silver Storage
                    │
                    ▼
              Gold Storage
                    │
                    ▼
             Report Manager
                    │
                    ▼
            Alert / Monitoring
"""
