import datetime
import pandas as pd
import numpy as np
import os
import sys
import pytz
from numpy.typing import ArrayLike, DTypeLike, NDArray
from typing import Sequence, List, Dict, Tuple, Set, Any, Union, Optional, Annotated, Callable, Literal, TypeVar
from loguru import logger

error_message: Dict[str, any] = {
    "check_mandatory": "[{} - Check mandatory] Required field.",
    "check_data_type": "[{} - Check data type] Data type must be '{}'.",
    "check_in_range_numeric": "[{} - Check in range numneric] Value must be in range [{}, {}].",
    "check_correct_datetime_format": "[{} - Check correct datetime format] Value must be correct format: '{}'.",
    "check_in_range_datetime": "[{} - Check in range datetime] Value must be in range [{}, {}].",
}

def add_message_function(message: str = "") -> set:
    return lambda _: _.union({message})

# ========== Config ==========
DATE_FORMAT: str = "%Y-%m-%d"
DATETIME_FORMAT: str = "%Y-%m-%d HH:MM:SS"
today: str = datetime.datetime.now().strftime(DATE_FORMAT)

DATA_RAW_FOLDER_PATH: str = "/home/user/data-da-ds-de/data_test/raw"
FILE_PATH: str = f"{DATA_RAW_FOLDER_PATH}/sales_data_sample.xlsx"
SHEET_NAME: str = "Sales_Data"
"Data_Issues"
"Monthly_Summary"
# "Inventory"
# "Customer_Data"
# "Sales_Data"

REPORT_FOLDER_PATH: str = "/home/user/data-da-ds-de/reports"
data_validation_report: str = f'{REPORT_FOLDER_PATH}/{today}.xlsx'
LOG_FOLDER_PATH: str = "/home/user/data-da-ds-de/logs"
log_file_path: str = f"{LOG_FOLDER_PATH}/{today}.log"

logger.remove()
logger.add(
    sys.stdout,
    colorize=True
)
logger.add(
    log_file_path,
    colorize=False,
)