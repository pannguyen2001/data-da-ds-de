import datetime
import os
from enum import StrEnum, auto
from pathlib import Path

import pytz
from dotenv import load_dotenv

# ========== Load environment variables from .env file ==========
load_dotenv()
# Access environment variables
PROJECT_NAME = os.getenv("PROJECT_NAME")
DB_URL = os.getenv("DB_URL")
API_KEY = os.getenv("API_KEY")
DEBUG_MODE = os.getenv("DEBUG")
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")

# ========== Timezone config ==========
local_timezone = pytz.timezone("Asia/Ho_Chi_Minh")
date_format = "%Y-%m-%d"
datetime_format = "%Y-%m-%d %H:%M:%S"
date_today = datetime.datetime.now().strftime(date_format)

# ========== Folder paths ==========
project_root = Path(__file__).parent.resolve()


# ====================
# Enums
# ====================


# ===== Commons =====
class DatetimeFormat(StrEnum):
    DATE_YEAR_FIRST = "%Y-%m-%d"
    DATETIME_YEAR_FIRST = "%Y-%m-%d %H:%M:%S"
    DATE_MONTH_FIRST = "%m-%d-%Y"
    DATETIME_MONTH_FIRST = "%m-%d-%Y %H:%M:%S"
    DATE_DAY_FIRST = "%d-%m-%Y"
    DATETIME_DAY_FIRST = "%d-%m-%Y %H:%M:%S"


class DataPipelineActivities(StrEnum):
    COLLECTION = auto()
    INGESTION = auto()
    COMPUTING = auto()
    STORAGE = auto()
    CONSUMPTION = auto()
    MANAGEMENT = auto()
    GOVERNANCE = auto()
    MONITORING = auto()
    REPORTING = auto()
    ANALYSIS = auto()
    VISUALIZATION = auto()
    PRESENTATION = auto()
    ALERTING = auto()
    LOGGING = auto()
    COMMON = auto()


class LoggerLevels(StrEnum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"
    TRACE = "TRACE"


# ===== Source =====
class FileType(StrEnum):
    CSV = auto()
    JSON = auto()
    PARQUET = auto()
    XLSX = auto()
    XLS = auto()
    YAML = auto()
    YML = auto()
    DB = auto()


class ResolveFileType(StrEnum):
    CSV = auto()
    JSON = auto()
    PARQUET = auto()
    EXCEL = auto()
    YAML = auto()
    SQL = auto()


class SourceType(StrEnum):
    FILE = auto()
    API = auto()
    DATABASE = auto()
    WEB = auto()
    OPENDB = auto()


class DbEngine(StrEnum):
    SQLITE = auto()
    POSTGRESQL = auto()
    MYSQL = auto()
    MONGODB = auto()
    DUCKDB = auto()


class ApiMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class DownloadSource(StrEnum):
    GGDRIVE = auto()
    HUGGINGFACE = auto()
    KAGGLE = auto()


# ===== Status =====
class OperationStatus(StrEnum):
    PASS = auto()
    FAIL = auto()
    SKIP = auto()
    PENDING = auto()
    RUNNING = auto()


# class PipelineStatus(StrEnum):
#     PENDING = auto()
#     ERROR = auto()
#     SKIP = auto()


class DownloadStatus(StrEnum):
    PENDING = auto()
    READY = auto()
    DOWNLOADING = auto()
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()
    DRY_RUN = auto()