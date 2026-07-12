from dataclasses import dataclass, field

from python_calamine import CalamineWorkbook

from src.common.constants import DownloadStatus, ResolveFileType
from src.common.detect_file_type import detect_file_type
from src.io.downloader.base import Downloader
from src.common.logger import logger
from src.io.reader.base import FileReader
from src.io.reader.registry import _READERS
from src.models.config.file_config import FileConfig
from src.models.result.download_result import DownloadResult
from src.io.connector.base import DatabaseConnector
from src.pipeline.task.base import BaseTask


@dataclass
class PreprocessSourceTask(BaseTask):
    always_run: bool = True
    file_type: ResolveFileType | None = None
    detailed: dict = field(default_factory=dict)

    def _preprocess_api(self):
        """
        Preprocess api.
        1. Load api config.
        2. Read data from API.
        3. Save data as parquet to staging.
        4. If data is not parquet, load data to parquet.
        5. Save to staging.
        """

        pass

    def _preprocess_web(self):
        """
        Preprocess web.
        1. Load web config.
        2. Read data from web.
        3. Save data as parquet to staging.
        4. If data is not parquet, load data to parquet.
        5. Save to staging.
        """

        pass

    def _preprocess_downloader(self, downloader: Downloader) -> None:
        """
        Preprocess downloader.
        1. Load downloader config.
        2. Download data from url.
        3. Convert result to file reader.
        """

        logger.info("Preprocess downloader process.")

        self.detailed["preprocessed_downloader"] = []
        self.detailed["skipped_downloader"] = []
        download_result: DownloadResult = downloader.execute()
        logger.info(f"Downloader result: {download_result.model_dump()}.")

        if download_result.status == DownloadStatus.SUCCESS:
            for file_downloaded in download_result.files_downloaded:
                try:
                    suffix: ResolveFileType = detect_file_type(file_downloaded)
                except Exception as e:
                    logger.error(e)
                    self.detailed["skipped_downloader"].append(
                        str(file_downloaded)
                    )
                    continue

                if suffix == ResolveFileType.EXCEL:
                    sheet_names = CalamineWorkbook.from_path(
                        file_downloaded
                    ).sheet_names

                    for sheet in sheet_names:
                        options = {"sheet_name": sheet}

                        reader: FileReader = _READERS[suffix](
                            FileConfig(
                                file_path=file_downloaded,
                                file_type=ResolveFileType.EXCEL,
                                options=options,
                            )
                        )
                        self.context.readers.append(reader)
                        self.detailed["preprocessed_downloader"].append(
                            str(file_downloaded) + " - " + sheet
                        )
                else:
                    reader = _READERS[suffix](
                        FileConfig(file_path=file_downloaded, file_type=suffix)
                    )
                    self.context.readers.append(reader)
                    self.detailed["preprocessed_downloader"].append(
                        str(file_downloaded)
                    )
        elif download_result.status == DownloadStatus.SKIPPED:
            self.detailed["skipped_downloader"].append(
                str(download_result.destination)
            )

        logger.info("Preprocess downloader complete.")

    def _execute(self):
        """Run preprocessing task. For API/web/opendb, connect and download to staging folder. Then create File reader for each file in staging folder. For file, detect and group file based on file name pattern (and sheet name if have). Then save to raw folder."""

        config: dict = self.context.setup.get("storage_config")
        self.file_type: ResolveFileType = config.get("file_type")

        # self._preprocess_api()

        # self._preprocess_web()

        if not self.context.downloaders:
            logger.info("No downloaders to preprocess.")
        else:
            for downloader in self.context.downloaders:
                self._preprocess_downloader(downloader)

    # Preprocessing
    # TODO
    # If need group data by file, ex: excel sheet A, A1, A2,.. having the same sheet name S1, S2,...; parquet file have the same file format: file_1.parquet, file_2.parquet,...; db table have the same table name: table_1, table_2,..., then group data by file, sheet, table name.
    # Staging: detect and group -> save as parquet -> transfer to raw
    # process mode: append, replace, onetime, incremental, just load update/delete/insert data, not load all or replace all. (SDC, CDC,...)
