import datetime
import json
import traceback
from typing import Any
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from src.common.config import checkpoint_file
from src.common.constants import DatetimeFormat, OperationStatus
from src.common.logger import logger
from src.io.loader.registry import _LOADERS
from src.models.metadata import MetaData


class Checkpoint(BaseModel):
    """Represents a checkpoint."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    task_name: str | None = None
    status: OperationStatus = Field(default=OperationStatus.PENDING)
    error: Exception | str | None = None
    detailed: Any | None = None

    # addition 2026-july-10
    run_id: UUID = Field(default_factory=uuid4)
    start_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_at: datetime.datetime | None = None
    duration: float | None = None
    retry: int = 0
    warnings: list[str] | None = None

    @field_serializer("start_at")
    def serialize_start_at(self, value: datetime.datetime):
        tz_value = (
            value
            if value.tzinfo
            else value.replace(tzinfo=ZoneInfo("Asia/Ho_Chi_Minh"))
        )
        return tz_value.strftime(DatetimeFormat.DATETIME_YEAR_FIRST.value)

    @field_serializer("end_at")
    def serialize_end_at(self, value: datetime.datetime | None):
        return (
            value.replace(tzinfo=ZoneInfo("Asia/Ho_Chi_Minh")).strftime(
                DatetimeFormat.DATETIME_YEAR_FIRST.value
            )
            if value
            else None
        )

    @field_serializer("run_id")
    def serialize_run_id(self, value: UUID):
        return str(value)

    def mark_passed(self):
        self.status = OperationStatus.PASS

    def mark_failed(self, error: Exception | str):
        self.error = "\n".join(
            traceback.TracebackException.from_exception(error).format()
        )
        self.status = OperationStatus.FAIL

    def mark_skipped(self):
        self.status = OperationStatus.SKIP

    def mark_pending(self):
        self.status = OperationStatus.PENDING

    def mark_running(self):
        self.status = OperationStatus.RUNNING

    def get_detailed(self, detailed: Any):
        self.detailed = detailed

    def finalize(self):
        if not self.start_at.tzinfo:
            self.start_at = self.start_at.replace(tzinfo=ZoneInfo("Asia/Ho_Chi_Minh"))
        self.end_at = datetime.datetime.now().replace(
            tzinfo=ZoneInfo("Asia/Ho_Chi_Minh")
        )
        self.duration = (self.end_at - self.start_at).total_seconds()


class CheckpointManager(BaseModel):
    """Manages the checkpointing of models."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: dict[str, Any] | None = Field(default_factory=dict)

    run_id: UUID = Field(default_factory=uuid4)
    results: list[Checkpoint] = Field(default_factory=list)
    metadata: MetaData = Field(default_factory=MetaData)

    @field_serializer("run_id")
    def serialize_run_id(self, value: UUID):
        return str(value)

    def load_checkpoint(self):
        if self.config is None:
            logger.info("No last checkpoint config. Run pipleine from start.")
            return self.result

        checkpoint_result = _LOADERS[self.config.get("file_type")](self.config).load()
        logger.info(f"Last checkpoint: {checkpoint_result}")

        if checkpoint_result.status != OperationStatus.PASS:
            return self.results

        if not checkpoint_result.data:
            logger.info("No last checkpoint data. Run pipleine from start.")
            return self.results

        self.results = [
            Checkpoint(**result) for result in checkpoint_result.data.get("results", [])
        ]
        return self.results

    def add_checkpoint(self, checkpoint: Checkpoint):
        self.results.append(checkpoint)

    def save_checkpoint(self):
        """Save checkpoint to file."""

        for cp in self.results:
            cp.finalize()

        self.metadata.end_at = datetime.datetime.now(datetime.timezone.utc).replace(
            tzinfo=ZoneInfo("Asia/Ho_Chi_Minh")
        )

        result = self.model_dump() if hasattr(self, "model_dump") else self.dict()
        del result["config"]

        with open(str(checkpoint_file), "w") as f:
            json.dump(result, f, indent=4)
