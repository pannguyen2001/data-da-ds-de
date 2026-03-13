import os
from pathlib import Path
import pandas as pd
import numpy as np


# First, load data
base_path: str = os.path.dirname(os.path.abspath(__file__))
data_folder_path: str = os.path.join(
    base_path, "data_test", "raw", "prevalidation_data_2503")
# print(data_folder_path)

master_data_setup_file_path = "/home/user/data-da-ds-de/data_validation_pandas/data_test/raw/prevalidation_data_2503/Data Template 03_Master Data Setup_SLP3P4 1.xlsx"

# Cross validation
df_suspension_reason: pd.DataFrame = pd.read_excel(
    master_data_setup_file_path, sheet_name="SuspensionReason")

internal_suspended_list_prequisite: list[dict] = [{
    "file_path": master_data_setup_file_path,
    "sheet_name": "SuspensionReason",
    "column_name": "Suspension reason name",
    "value": "All"
}]

internal_suspended_list_validation_config: dict = {
    "file_path": master_data_setup_file_path,
    "sheet_name": "InternalSuspendedList",
    "properties": {
        "ID":{
            "type": "str",
            "required": True,
            "min_length": 1,
            "max_length": 10,
            "format": "^IS\d{5}",
            "unique": True
        },
        "Debtor type": {
            "type": "str",
            "required": True,
            "unique": False,
            "value_list": ["Individual", "Company"]
        },
        "NRIC/FIN": {
            "type": "str",
            "required": True,
            "min_length": 9,
            "max_length": 10,
            "unique": True,
        },
        "UEN": {
            "type": "str",
            "required": True,
            "min_length": 9,
            "max_length": 10,
            "unique": True,
        },
        "Effective from": {
            "type": "date",
            "required": True,
            "format": "%d/%m/%Y",
            "min_length": "01/01/1900",
            "max_length": "31/12/2099",
            "unique": False
        },
        "Effective to": {
            "type": "date",
            "format": "%d/%m/%Y",
            "min_length": "01/01/1900",
            "max_length": "31/12/2099",
            "unique": False,
            "required": False
        },
        "Bad debt write-off amount": {
            "type": "float",
            "min_length": 0,
            "max_length": 999999999999.99,
            "unique": False,
            "required": False
        },
        "Suspended reason": {
            "type": "str",
            "required": True,
            "unique": False
        },
        "Remarks": {
            "type": "str",
            "min_length": 0,
            "max_length": 255,
            "unique": False,
            "required": False
        },
        "Status": {
            "type": "str",
            "required": True,
            "value_list": ["Active", "Inactive"],
            "unique": False
        },
        "Created By": {
            "type": "str",
            "min_length": 1,
            "max_length": 50,
            "unique": False,
            "required": False
        },
        "Created On": {
            "type": "datetime",
            "format": "%d/%m/%Y %H:%M:%S",
            "min_length": "01/01/1900 00:00:00",
            "max_length": "31/12/2099 23:59:59",
            "unique": False,
            "required": False
        },
        "Modified By": {
            "type": "str",
            "min_length": 0,
            "max_length": 50,
            "unique": False,
            "required": False
        },
        "Modified On": {
            "type": "datetime",
            "format": "%d/%m/%Y %H:%M:%S",
            "min_length": "01/01/1900 00:00:00",
            "max_length": "31/12/2099 23:59:59",
            "unique": False,
            "required": False
        },
    }
}

internal_suspended_list_preprocessing_config: dict = {
    "ID": {
        "fill_default": None, # if having defaulr, ignore fillna
        "fillna": pd.NA, # if not having default, use fillna, must match convert_dtype, if string -> fill with "", int -> fill with 0, float -> fill with 0.0, list -> fill with [], dict -> fill with {}, etc
        "mapping": None,
        "separator": None,
        "convert_dtype": str, # convert to string, because convert_dtypes() sometime can not convert data to string correctly if data contain int or float
        "white_space": None,
        "lower_case": None,
        "upper_case": None
    }
}

# Preprocessing
# - Fill default
# - Fillna
# - Mapping
# - Separator
# - Convert dtype
# - Remove white space
# - Lower case
# - Upper case

from validations.master_data_setup.internal_suspended_list import internal_suspended_list_validation

internal_suspended_list_validation_result = internal_suspended_list_validation( internal_suspended_list_validation_config, internal_suspended_list_prequisite)
# Process result
internal_suspended_list_validation_result["validation_result"] = internal_suspended_list_validation_result["validation_result"].map(lambda x: sorted(x))
internal_suspended_list_validation_result["validation_result"] = internal_suspended_list_validation_result["validation_result"].map(lambda x: "\n".join(x))
internal_suspended_list_validation_result = internal_suspended_list_validation_result.replace("nan", np.nan)
# print(internal_suspended_list_validation_result)
# Write to Excel
from helpers.write_data_to_excel_file import write_data_to_excel_file
write_data_to_excel_file(internal_suspended_list_validation_result, "internal_suspended_list_validation_result.xlsx", sheet_name="InternalSuspendedList")
