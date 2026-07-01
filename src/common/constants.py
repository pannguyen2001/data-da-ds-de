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


# ========== Data pipeline phase ==========
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


class ReaderStatus(StrEnum):
    PASS = auto()
    FAIL = auto()

class PipelineStatus(StrEnum)
    PENDING = auto()
    ERROR = auto()
    SKIP = auto()
