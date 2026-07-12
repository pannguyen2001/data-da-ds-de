from pydantic import BaseModel

from src.common.constants import SourceType
from src.models.config.api_config import ApiConfig
from src.models.config.db_connector_config import DbConfig
from src.models.config.file_config import FileConfig
from src.models.config.download_config import DownloadConfig


class SourceConfig(BaseModel):
    name: str
    source_type: SourceType
    config: FileConfig | ApiConfig | DbConfig | DownloadConfig

    # TODO: Add mode: a: append, w: replace and write, o: onetime only load, i: incremental load
