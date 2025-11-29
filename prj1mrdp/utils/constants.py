import os
import datetime
import pytz
from pathlib import Path
from dotenv import load_dotenv

def create_file(folder_path: str= "", file_name: str = ""):
    """
    Create file in folder

    Args:
        folder_path (str, optional): Folder path. Defaults to "".
        file_name (str, optional): File name. Defaults to "".

    Returns:
        Path: File path.
    """
    try:
        file_path = os.path.join(folder_path, file_name)
        file_path = Path(file_path)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        return file_path
    except Exception as e:
        print(f"Error creating file: {e}")
        return None

# # ========== Load environment variables from .env file ==========
# load_dotenv()

# # Access environment variables
# database_url = os.getenv('DATABASE_URL')
# api_key = os.getenv('API_KEY')
# debug_mode = os.getenv('DEBUG')

# print(f"Database URL: {database_url}")
# print(f"API Key: {api_key}")
# print(f"Debug Mode: {debug_mode}")

# ========== Timezone config ==========
local_timezone = pytz.timezone("Asia/Ho_Chi_Minh")
date_format = "%Y-%m-%d"
datetime_format = "%Y-%m-%d %H:%M:%S"

# ========== Logging config ===========
today = datetime.datetime.now().strftime(date_format)
log_file = f"{today}.log"
log_folder = "./logs"
output_log_file = create_file(log_folder, log_file)

# Debug
error_log_file = "tracking_error.log"
error_log_file = create_file(log_folder, error_log_file)

# ========== Database config ===========
# Test database
db_folder: str = "./database/test"
raw_db_file_path: str = create_file(db_folder, "0_raw.db")
brozen_db_file_path: str = create_file(db_folder, "1_brozen.db")
silver_db_file_path: str = create_file(db_folder, "2_silver.db")
golden_db_file_path: str = create_file(db_folder, "3_golden.db")

# ========== Data ==========
data_folder: str = "./data/test"
raw_data_folder: str = create_file(data_folder, "0_raw")
brozen_data_folder: str = create_file(data_folder, "1_brozen")
silver_data_folder: str = create_file(data_folder, "2_silver")
golden_data_folder: str = create_file(data_folder, "3_golden")

# =========== Report ==========
report_folder: str = f"./reports/{today}"
Path(report_folder).mkdir(exist_ok=True, parents=True)



