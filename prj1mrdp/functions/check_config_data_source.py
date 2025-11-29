import uuid
import os
import datetime
import pandas as pd
import numpy as np
from typing import Dict
from requests import Response, post, get
from helpers import write_data_to_excel_file
from helpers.logger import collection_phase_logger
from utils.constants import local_timezone, date_format

# validate config data
# check source source_status: can access or not
# export report: excel and pdf/word
# tracking history checksource and report
# history: id, phase - sub phase, time, action, data, result, evidence storage (report path,..)
# log, alert
# if first load
# if not first load
# status: data validation failed: when data is not meet requirement, ready for collect: valid data and api/file can get data, error: get data failed

local_datetime = local_timezone.localize(datetime.datetime.now()).strftime(date_format)
checking_config_logger = collection_phase_logger.bind(sub_phase="checking_config")
boolean_value_mapping: Dict = {
    True: "true",
    False: "false"
}
error_message_formats: Dict = {
        "required": "[{}] Required field.",
        "invalid_value": "[{}] Invalid value. Correct value is one of these: '{}'.",
        "refered_required": "[{}] Required when field '{}' is '{}'.",
        "refered_invalid_value": "[{}] Invalid refered value. Value must be one of these: '{}' when field '{}' is/are '{}'.",
        "invalid_format": "[{}] Incorrect format. Correct format is '{}'."
    }

# @checking_config_logger.catch
# def is_empty(df: pd.DataFrame, column_name: str = ""):
#     """
#     """

#     error_message: str = error_message_formats["required"]
#     if column_name not in df.columns:
#         raise ValueError(f"Column '{column_name}' does not exist in data")

#     mask = df[column_name].isna()
#     df["error"] = df.apply()
#     if mask.any():
#         pass



# @checking_config_logger.catch
# def validate_config_data(df: pd.DataFrame):
#     """
#     Validate config data

#     Args:
#         df (pd.DataFrame): config data
#     """
#     # Check empty
#     if df.empty:
#         checking_config_logger.error("Config file is empty.")
    
#     # Check refered empty
#     df["is_first_load"] = df["is_first_load"].map(lambda x: boolean_value_mapping[x])
#     df.loc[df["created_at"].isna(), "created_at"] = local_datetime
#     df = df.fillna("")

#     df["source_id"] = df.apply(lambda x: str(uuid.uuid4()) if pd.isna(x["source_id"]) and x["is_first_load"] else x["source_id"], axis=1)
#     checking_config_logger.info(df[["source_status", "is_first_load"]])

#     # df1 = df1.loc[df["is_first_load"]==False, :]
#     # if not df1.empty:
#     #     df1 = df.loc[df["source_status"]=="active", :]
#     #     if df1.empty:
#     #         checking_config_logger.warning(f"No active source.")
#     #         return None

#     # df = df.reset_index(drop=True)
#     checking_config_logger.info(f"Config file has {len(df)} active config.")
#     return df

# @checking_config_logger.catch
# def is_exixt_path(path: str):
#     if not os.path.exists(path):
#         raise ValueError(f"Path '{path}' does not exist")
#     checking_config_logger.info(f"Path '{path}' exist")
#     return True

# @checking_config_logger.catch
# def check_api_source(api_source_path: str = "", method: str = "POST"):
#     message: str = ""
#     if method == "GET":
#         response: Response = get(api_source_path)
#     elif method == "POST":
#         response: Response = post(api_source_path)

#     if response.status_code >= 400 and response.status_code < 500 :
#         message: str = f"""
#         [WARNING]
#         API source '{api_source_path}' is not working.
#         Method: {method}
#         Response status code: {response.status_code}
#         Response: {response.text}
#         """
#         checking_config_logger.warning(message)
#         return False, message

#     checking_config_logger.info(f"API source '{api_source_path}' is ready for next phase.")
#     return True, message


# # @checking_config_logger.catch
# # def check_config(config_file_path: str = ""):
    # """
    # Check config file

    # Args:
    #     config_file_path (str): config file path
    # """
    # checking_config_logger.info(f"Checking config file '{config_file_path}'")
    # if not is_exixt_path(config_file_path):
    #     return None

    # df = pd.read_excel(config_file_path)
    # if df.empty:
    #     checking_config_logger.warning(f"Config file '{config_file_path}' is empty")
    #     return None

    # df = validate_config_data(df)
    # if df is None:
    #     return None

    # for index, row in df.iterrows():
    #     if row["source_id"] in [np.nan, ""]:
    #         df.loc[index, "source_id"] = str(uuid.uuid4())
    #         checking_config_logger.info(f"No source id in row '{index + 2}'. Created new id: {df.loc[index, "source_id"]}'")
    #     source_type: str = row["source_type"].strip().lower()
    #     source_path: str = row["source_path"].strip()
    #     action: str = row["action"].strip()

    #     if source_type not in ["csv", "excel", "api", "json", "web_table", "sql"]:
    #         df.loc[index, "error"] = f"Source type '{source_type}' is not supported"
    #         checking_config_logger.warning(df.loc[index, "error"])
    #         continue

    #     if source_type == "api":
    #         method: str = row["api_method"].strip().upper()
    #         if method not in ["GET", "POST"]:
    #             df.loc[index, "error"] = f"Method '{method}' is not supported"
    #             checking_config_logger.warning(df.loc[index, "error"])
    #             continue
    #         df.loc[index, "source_status"], df.loc[index, "error"] = check_api_source(source_path, method)
    #     elif source_type in ["csv", "excel", "json"]:
    #         if action == "load":
    #             if not is_exixt_path(source_path):
    #                 df.loc[index, "source_status"] = False
    #                 df.loc[index, "error"] = f"Source path '{source_path}' does not exist"
    #                 checking_config_logger.warning(row["error"])
    #             df.loc[index, "source_status"] = True

    #     df.loc[index, "updated_at"] = local_datetime
    #     df.loc[index, "is_first_load"] = False

    # df["source_status"] = df["source_status"].map(lambda x: "active" if x else "error")
    # df["is_first_load"] = df["is_first_load"].map(lambda x: str(x).lower())

    # checking_config_logger.info(f"Complete checking config file: '{config_file_path}'")
    # # for column in df.columns:
    # #     checking_config_logger.info(f"Detail: \n{df[column]}")
    # write_data_to_excel_file(df, f"./reports/{local_datetime}.xlsx", "COLLECTION_check_config")
    # return True
    

