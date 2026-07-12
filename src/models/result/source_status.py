from pydantic import Field, BaseModel

from src.models.config.api_config import ApiConfig
from src.models.config.download_config import DownloadConfig
from src.models.metadata import MetaData


class SourceStatus(BaseModel):
    config: ApiConfig | DownloadConfig
    reachable: bool = False
    http_status: int | None = None
    content_type: str | None = None
    content_length: int | None = None
    error: str | None = None
    metadata: MetaData = Field(default_factory=MetaData)