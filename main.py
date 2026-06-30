from constants import date_today
from utils.create_io_entry import create_io_entry


# ==========================================
# Folder paths
# ==========================================

# ========== Database ===========
db_folder: str = "./database"
staging_db_file_path: str = create_io_entry(db_folder + "/0_staging")
brozen_db_file_path: str = create_io_entry(db_folder + "/1_brozen")
silver_db_file_path: str = create_io_entry(db_folder + "/2_silver")
golden_db_file_path: str = create_io_entry(db_folder + "/3_golden")
test_db_file_path: str = create_io_entry(db_folder + "/4_test")

# ========== Data ==========
data_folder: str = "./data"
staging_data_folder: str = create_io_entry(data_folder + "/0_staging")
brozen_data_folder: str = create_io_entry(data_folder + "/1_brozen")
silver_data_folder: str = create_io_entry(data_folder + "/2_silver")
golden_data_folder: str = create_io_entry(data_folder + "/3_golden")
test_data_folder: str = create_io_entry(data_folder + "/4_test")

# =========== Report ==========
report_folder: str = f"./reports/{date_today}"
create_io_entry(report_folder)
