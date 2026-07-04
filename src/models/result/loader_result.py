from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import OperationStatus
from src.models.metadata import MetaData


class LoaderResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: list | Any
    source: Path
    size_mb: float | None
    status: OperationStatus
    error: Exception | str | None
    metadata: MetaData = Field(default_factory=MetaData)
