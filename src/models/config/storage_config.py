import datetime
from pathlib import Path
from typing import Any, Literal

import polars as pl
from pydantic import BaseModel, ConfigDict, Field

from src.common.constants import DatetimeFormat


class StorageConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    df: pl.LazyFrame | None
    des_folder_path: Path = Field(default_factory=Path)
    des_file_name: str = Field(default_factory=lambda: f"unknown_{datetime.datetime.now().strftime(DatetimeFormat.DATETIME_YEAR_FIRST.value)}")
    options: dict[str, Any] | None = Field(default_factory=dict)
    mode: Literal["a", "w", "i"] = (
        "w"  # a: append, w: drop all and write, i: incremntal loader, default "w"
    )
