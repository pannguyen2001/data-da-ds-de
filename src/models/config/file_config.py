from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic.fields import Field

from src.common.constants import ResolveFileType


class FileConfig(BaseModel):
    file_path: Path
    file_type: ResolveFileType
    options: dict[str, Any] | None = Field(default_factory=dict)
