import pandas as pd
import numpy as np
from loguru import logger
from typing import List, Optional
from helpers import (
    check_mandatory,
    check_unique,
    check_in_range_datetime,
    check_correct_datetime_format,
    check_in_range_numeric,
    check_in_range_string_length,
    check_int,
    check_numeric,
    check_in_value_list
)
from utils.constant import  add_message_function

@logger.catch
def internal_suspended_list_validation( config: dict, prequisite: dict) -> Optional[pd.DataFrame]:
    """
    Validate the internal suspended list

    Args:
        df (pd.DataFrame): The dataframe to validate
        config (dict): The configuration for the validation
        prequisite (dict): The prequisite for the validation

    Returns:
        pd.DataFrame: The validated dataframe
    """
    # get data for validation
    df: pd.DataFrame = pd.read_excel(
    config["file_path"], sheet_name=config["sheet_name"])
    df = df.apply(lambda x: x.astype(str).str.strip(), axis=1).convert_dtypes()

    if df is None or df.empty:
        logger.error("Dataframe is empty.")
        return

        # get prequisite
    if not prequisite:
        logger.info("Prequisite is empty.")

    df_suspension_reason: pd.DataFrame = pd.read_excel(
        prequisite[0]["file_path"], sheet_name=prequisite[0]["sheet_name"])
    if df_suspension_reason is None or df_suspension_reason.empty:
            logger.error("Dataframe is empty.")
            return
    suspension_reason_name: List[str] = df_suspension_reason[prequisite[0]["column_name"]].tolist()

    for column, detail_config in config["properties"].items():
        for key, value in detail_config.items():
            # Check data type
            # Check mandatory
            # Check unique
            # Check correct datetime format or string format
            # Check in range datetime
            # Check in range string length
            # Check in range numeric (int and float)
            # Check in value list
            # Check special logic for columns in table
            # Check cross-validation (for table and extenal tables)
            # if return df -> log error and continue
            # should separate df and validation result, meaning validation result just is a series has the same index as df, not change df, should not let df is depend on previous result
            # Redesign: validation_result: pd.Series = pd.Series([set() for _ in range(df.shape[0])], name="validation_result", index=df.index)
            # if key == "xxx" and value:
            # temp_validation_result_mask = check_xxx(df, column)
            # validation_result.loc[temp_validation_result_mask] = validation_result[temp_validation_result_mask].map(add_message_function(message))

            # if key == "required" and value:
            #     df = check_mandatory(df, column)
            # if key == "unique" and value:
            #     df = check_unique(df, column)
            # if key =="type" and value == "str" and "min_length" in detail_config and "max_length" in detail_config:
            #     df = check_in_range_string_length(df, column, (detail_config["min_length"], detail_config["max_length"]))
            # if key =="type" and value in ["date", "datetime"]:
            #     df = check_correct_datetime_format(df, column, detail_config["format"])
            #     df = check_in_range_datetime(df, column, datetime_range=(detail_config["min_length"], detail_config["max_length"]), datetime_format=detail_config["format"])
            # if key =="type" and value == "int":
            #     df = check_int(df, column)
            #     df = check_in_range_numeric(df, column, (detail_config["min_length"], detail_config["max_length"]))
            # if key == "type" and value == "float":
            #     df = check_numeric(df, column)
            #     df = check_in_range_numeric(df, column, (detail_config["min_length"], detail_config["max_length"]))
            if key == "value_list" and value:
                df[column] = df[column].str.strip().str.title()
                df = check_in_value_list(df, column, detail_config["value_list"])

    # # Special logic for columns in table
    # df_cross_validation = df.copy(deep=True)
    # # df["validation_result"] = [set() for _ in range(df.shape[0])]
    # # Check Eff from <= Eff to
    # df_cross_validation["Effective from"] = pd.to_datetime(df_cross_validation["Effective from"], format="%d/%m/%Y", errors="coerce")
    # df_cross_validation["Effective to"] = pd.to_datetime(df_cross_validation["Effective to"], format="%d/%m/%Y", errors="coerce")
    # incorrect_eff_to_mask: pd.Series = df_cross_validation["Effective from"] > df_cross_validation["Effective to"]
    # if incorrect_eff_to_mask.any():
    #     df.loc[incorrect_eff_to_mask, "validation_result"] = df.loc[incorrect_eff_to_mask, "validation_result"].map(add_message_function(
    #         "[Effective from - Effective to][Incorrect datetime logic] Effective from must be less than or equal to Effective to"
    #     ))

    # df_cross_validation["Created On"] = pd.to_datetime(df_cross_validation["Created On"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    # df_cross_validation["Modified On"] = pd.to_datetime(df_cross_validation["Modified On"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    # incorrect_modified_on_mask: pd.Series = df_cross_validation["Created On"] > df_cross_validation["Modified On"]
    # if incorrect_modified_on_mask.any():
    #     df.loc[incorrect_modified_on_mask, "validation_result"] = df.loc[incorrect_modified_on_mask, "validation_result"].map(add_message_function(
    #         "[Created On - Modified On][Incorrect datetime logic] Created On must be less than or equal to Modified On"
    #     ))

    # # Cross validation
    # suspension_reason_not_empty_mask: pd.Series = df_cross_validation["Suspended reason"].replace("", np.nan).replace("nan", np.nan).notna()
    # incorrect_refered_values = df_cross_validation["Suspended reason"].map(lambda x: x not in suspension_reason_name)
    # incorrect_refered_values &= suspension_reason_not_empty_mask

    # if incorrect_refered_values.any():
    #     df.loc[incorrect_refered_values, "validation_result"] = df.loc[incorrect_refered_values, "validation_result"].map(add_message_function(
    #         "[Suspended reason][Incorrect refered values] Suspended reason must be in the list of suspended reason"
    #     ))

    return df