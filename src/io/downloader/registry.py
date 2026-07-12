from src.common.constants import DownloadSource
from src.io.downloader.base import Downloader
from src.io.downloader.ggdrive import GoogleDriveDownloader
from src.io.downloader.huggingface import HuggingFaceDownloader
from src.io.downloader.kaggle import KaggleDownloader

_DOWNLOADERS: dict[DownloadSource, type[Downloader]] = {
    DownloadSource.GGDRIVE: GoogleDriveDownloader,
    DownloadSource.HUGGINGFACE: HuggingFaceDownloader,
    DownloadSource.KAGGLE: KaggleDownloader,
}
