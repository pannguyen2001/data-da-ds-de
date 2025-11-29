import datetime
import pandas as pd
import numpy as np
import os
import sys
import pytz
from numpy.typing import ArrayLike, DTypeLike, NDArray
from typing import Sequence, List, Dict, Tuple, Set, Any, Union, Optional, Annotated, Callable, Literal, TypeVar
from loguru import logger
from data_validation import *
from helpers.write_data_to_excel_file import write_data_to_excel_file
from utils.constant import *

# =========== Load data ==========
df = pd.read_excel(FILE_PATH, SHEET_NAME)


# ========== Initial data exploratory (IDA) ==========
# IDA config
logger.info(df.info())


# Convert dtype to matches type
df = df.convert_dtypes()

# classify data by type
# int type
int_column_list: List = df.select_dtypes(include="int").columns.tolist()
# float type
float_column_list: List = df.select_dtypes(include="float").columns.tolist()
# number type
number_column_list: list = df.select_dtypes(include="number").columns.tolist()
# bool type
bool_column_list: list = df.select_dtypes(include="bool").columns.tolist()
# string type
str_column_list: list = df.select_dtypes(include="string").columns.tolist()
# datetime type
datetime_column_list: list = df.select_dtypes(include="datetime").columns.tolist()
# object type
object_column_list: list = df.select_dtypes(include="object").columns.tolist()

# Check empty for all column, except validation resul
empty_checked_column_list: List = df.columns.to_list()

# Print detail info
logger.info(f'''Summary detail info:
- File: {FILE_PATH}
- Sheet: {SHEET_NAME}
- Shape: {df.shape}
- Column: {empty_checked_column_list}
- Int type: {int_column_list}
- Float type: {float_column_list}
- Number type: {number_column_list}
- Bool type: {bool_column_list}
- String type: {str_column_list}
- Datetime type: {datetime_column_list}
- Object type: {object_column_list}''')

df["validation_result"] = [set() for _ in range(df.shape[0])]

# =========== Data validation ==========
# The way validation data, processing or transforming is depended on data source we meet, no common method. All are based on data.

# Group by data type and validation
# Check empty
if empty_checked_column_list:
    for col in empty_checked_column_list:
        check_mandatory(df, col)

# check number type
if number_column_list:
    for col in number_column_list:
        check_numeric(df, col)

# check correct datetime format
if datetime_column_list:
    for col in datetime_column_list:
        check_correct_datetime_format(df, col, DATETIME_FORMAT)
    # # Now, in sample_sale_data.xlsx > Sales_Data, having column "Month" has type "string", but it is datetime string, format "%Y-%m", so check format here
    # check_correct_datetime_format(df, "Month", "%Y-%m")

# ========== Data validation report ===========
# Process before write report
df["validation_result"] = df["validation_result"].map(lambda _: "\n".join(_))
excel_index: pd.Series = df.index + 2
df.insert(0, "Excel_Index", excel_index)
df_report: pd.DataFrame = df[df["validation_result"] != ""]

# Write to report
if df_report.empty:
    logger.success("No data to report. Data has no issue.")
else:
    logger.info("Write to report")
    write_data_to_excel_file(df_report, data_validation_report, SHEET_NAME)
    logger.success("Data saved")

# ========== Preprocessing data ===========


# ========== Trasforming data ==========
# # split date time to seperate month, year, day
# df["Year"] = pd.to_datetime(df["Date"], errors="coerce").dt.year
# df["Month"] = pd.to_datetime(df["Date"], errors="coerce").dt.month
# df["Day"] = pd.to_datetime(df["Date"], errors="coerce").dt.day