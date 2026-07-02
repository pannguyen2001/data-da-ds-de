from pydantic import BaseModel
from typing import Any

from src.common.constants import ApiMethod


class ApiConfig(BaseModel):
    url: str
    method: ApiMethod
    options: dict[str, Any] | None = None