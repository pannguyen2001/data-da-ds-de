import sys
from loguru import logger
from string import Template
import os
from datetime import datetime
from enum import Enum

# ========== Config ==========

# Date formats
class DatetimeFormat(Enum):
    DATE_FORMAT_V1: str = "%Y-%m-%d"
    DATE_FORMAT_V2: str = "%d-%m-%Y"
    DATETIME_FORMAT_V1: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT_V2: str = "%d-%m-%Y %H:%M:%S"

date_today: str = datetime.now().strftime(DATE_FORMAT_V1)
datetime_today: str = datetime.now().strftime(DATETIME_FORMAT_V1)


# ========== Folders ==========

# Logs folder
os.makedirs("logs", exist_ok=True)

# Reports folder
os.makedirs("reports", exist_ok=True)