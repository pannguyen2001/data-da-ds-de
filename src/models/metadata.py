import datetime

from pydantic import BaseModel, Field


class MetaData(BaseModel):
    start_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_at: datetime.datetime | None = None
