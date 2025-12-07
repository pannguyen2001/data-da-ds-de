import datetime
import sys
import sys
import os
from typing import  Dict, Any
from loguru import logger

error_message: Dict[str, any] = {
    "check_mandatory": "[{}][Check mandatory] Required field.",
    "check_data_type": "[{}][Check data type] Data type must be '{}'.",
    "check_in_range_numeric": "[{}][Check in range numeric] Value must be in range [{}, {}].",
    "check_correct_datetime_format": "[{}][Check correct datetime format] Value must be correct format: '{}'.",
    "check_in_range_datetime": "[{}][Check in range datetime] Value must be in range [{}, {}].",
    "check_in_range_string_length": "[{}][Check in range string length] Data length must be in range [{}, {}]."
}

def add_message_function(message: str = "") -> set:
    return lambda _: _.union({message})

# ========== Config ==========
DATE_FORMAT: str = "%Y-%m-%d"
DATETIME_FORMAT: str = "%Y-%m-%d HH:MM:SS"
today: str = datetime.datetime.now().strftime(DATE_FORMAT)

# Get origin directory
origin_dir_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_FOLDER_PATH: str = f"{origin_dir_path}/data_test/raw"
if not os.path.exists(DATA_RAW_FOLDER_PATH):
    os.makedirs(DATA_RAW_FOLDER_PATH)
FILE_PATH: str = f"{DATA_RAW_FOLDER_PATH}/sales_data_sample.xlsx"
SHEET_NAME: str = "Sales_Data"
"Data_Issues"
"Monthly_Summary"
# "Inventory"
# "Customer_Data"
# "Sales_Data"

REPORT_FOLDER_PATH: str = f"{origin_dir_path}/reports"
data_validation_report: str = f'{REPORT_FOLDER_PATH}/{today}.xlsx'
if not os.path.exists(REPORT_FOLDER_PATH):
    os.makedirs(REPORT_FOLDER_PATH)
LOG_FOLDER_PATH: str = f"{origin_dir_path}/logs"
log_file_path: str = f"{LOG_FOLDER_PATH}/{today}.log"
if not os.path.exists(LOG_FOLDER_PATH):
    os.makedirs(LOG_FOLDER_PATH)

logger.remove()
logger.add(
    sys.stdout,
    colorize=True
)
logger.add(
    log_file_path,
    colorize=False,
)