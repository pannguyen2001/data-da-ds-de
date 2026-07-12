from typing import Any

from dataclasses import dataclass, field

from src.io.connector.base import DatabaseConnector
from src.io.downloader.base import Downloader
from src.io.reader.base import FileReader
from src.checkpoint.manager import CheckpointManager


@dataclass
class PipelineContext:
    setup: dict[str, Any] = field(default_factory=dict)
    readers: list[FileReader] = field(default_factory=list)
    dbconnectors: list[DatabaseConnector] = field(default_factory=list)
    downloaders: list[Downloader] = field(default_factory=list)
    checkpoint: CheckpointManager = field(default_factory=CheckpointManager)
    # report: ReportManager = field(default_factory=ReportManager)
    # metrics: Metrics = field(default_factory=Metrics)
    metadata: dict[str, Any] = field(default_factory=dict)