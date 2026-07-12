import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_serializer

from src.common.constants import OperationStatus, DatetimeFormat


class MetaData(BaseModel):
    start_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_at: datetime.datetime | None = None

    @field_serializer("start_at")
    def _start_at_serializer(self, value: datetime.datetime) -> str:
        return value.strftime(DatetimeFormat.DATETIME_YEAR_FIRST.value)

    @field_serializer("end_at")
    def _end_at_serializer(self, value: datetime.datetime | None) -> str | None:
        return value.strftime(DatetimeFormat.DATETIME_YEAR_FIRST.value) if value else None

class PipelineMetaData(BaseModel):

    run_id: UUID = Field(default_factory=uuid4)
    pipeline_name: str | None = None
    start_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_at: datetime.datetime | None = None
    duration: float | None = None
    status: OperationStatus | None = None
    total_sources: int | None = None
    successful_sources: int | None = None
    failed_sources: int | None = None