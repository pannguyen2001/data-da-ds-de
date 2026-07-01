from pathlib import Path
from typing import Any, Mapping

from pydantic import BaseModel, Field


class ReaderConfig(BaseModel):
    """Reader config class."""

    file_path: Path = Field(default_factory=Path)
    options: Mapping[str, Any] = Field(default_factory=dict)


# ReaderConfig(Path("./"), {}).model_dump()
