from pathlib import Path

from pydantic import BaseModel, ConfigDict

from src.common.constants import OperationStatus
from src.models.metadata import MetaData


class StorageResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    destination: Path
    size_mb: float | None
    status: OperationStatus
    metadata: MetaData
