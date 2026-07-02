from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic.fields import Field


class FileConfig(BaseModel):
    file_path: Path
    options: dict[str, Any] | None = Field(default_factory=dict)
