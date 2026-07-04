from src.common.downloader.base import Downloader
from src.common.downloader.ggdrive import GoogleDriveDownloader
from src.common.downloader.huggingface import HuggingFaceDownloader
from src.common.downloader.kaggle import KaggleDownloader
from src.common.constants import DownloadSource

_DOWNLOADERS: dict[DownloadSource, type[Downloader]] = {
    DownloadSource.GGDRIVE: GoogleDriveDownloader,
    DownloadSource.HUGGINGFACE: HuggingFaceDownloader,
    DownloadSource.KAGGLE: KaggleDownloader
}