import datetime
import requests
import traceback
from typing import Union

from src.models.config.api_config import ApiConfig
from src.models.config.download_config import DownloadConfig
from src.models.result.source_status import SourceStatus
from src.models.metadata import MetaData


def check_source_status(config: Union[ApiConfig, DownloadConfig]) -> SourceStatus:
    try:
        """
        Make a request to the API endpoint.

        Args:
            config (SourceConfig): The configuration for the API endpoint.

        Returns:
            SourceStatus: The status of the API endpoint. If the endpoint is reachable, the status will contain the HTTP status code, content type, and content length. If the endpoint is not reachable, the status will contain the HTTP status code and an error message.
        """

        response = requests.head(
            config.url,
            timeout=1_000,
            allow_redirects=True,
        )

        response.raise_for_status()

        length = response.headers.get("Content-Length")

        return SourceStatus(
            config=config,
            reachable=True,
            http_status=response.status_code,
            content_type=response.headers.get("Content-Type"),
            content_length=int(length) if length else None,
            metadata=MetaData(end_at=datetime.datetime.now()),
        )

    except Exception as e:
        response = getattr(e, "response", None)

        return SourceStatus(
            config=config,
            reachable=False,
            http_status=getattr(response, "status_code", None),
            error="\n".join(traceback.TracebackException.from_exception(e).format()),
            metadata=MetaData(end_at=datetime.datetime.now()),
        )