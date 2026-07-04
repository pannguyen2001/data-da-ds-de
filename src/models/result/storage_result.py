from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import OperationStatus
from src.models.metadata import MetaData


class StorageResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    destination: Path
    size_mb: float | None
    status: OperationStatus
    error: Exception | str | None
    metadata: MetaData = Field(default_factory=MetaData)
