from typing import Any

from pydantic import BaseModel, Field

from src.common.constants import ApiMethod


class ApiConfig(BaseModel):
    url: str
    method: ApiMethod
    options: dict[str, Any] | None = Field(default_factory=dict)
