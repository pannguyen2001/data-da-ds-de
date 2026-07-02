from pydantic import BaseModel
from pathlib import Path
from typing import Any

class FileConfig(BaseModel):
    file_path: Path
    options: dict[str, Any] | None = None
