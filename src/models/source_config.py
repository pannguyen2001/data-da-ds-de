from pathlib import Path
from typing import Any, Mapping

from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    file_path: Path
    options: Mapping[str, Any] = Field(default_factory=dict)
