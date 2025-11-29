import datetime
import pandas as pd
import numpy as np
import os
import sys
import pytz
from numpy.typing import ArrayLike, DTypeLike, NDArray
from typing import Sequence, List, Dict, Tuple, Set, Any, Union, Optional, Annotated, Callable, Literal, TypeVar
from loguru import logger
from .is_empty import is_empty
from utils.constant import error_message, add_message_function

# ---------- Check datetime format ----------
@logger.catch
def is_correct_datetime_format(
    sr: pd.Series = None,
    input_format: str = "%Y-%m-%d"
    ) -> pd.Series:
    """Return True in each cell if can be converted to datetime follow format, else False."""
    return pd.to_datetime(sr, errors="coerce", format=input_format).notna()

@logger.catch
def check_correct_datetime_format(df: pd.DataFrame = None, column_name: str = "", datetime_format: str = "%Y-%m-%d") -> pd.DataFrame:
    """Return error message if cell value is incorrect datetime format else no message. Ignore empty value."""
    message: str = error_message["check_correct_datetime_format"].format(column_name, datetime_format)

    empty_mask: pd.Series = is_empty(df[column_name])

    correct_format_mask: pd.Series = is_correct_datetime_format(df[column_name], datetime_format)

    # Invalid value is:
    # - Not empty
    # - Wrong input format
    mask: pd.Series = ~empty_mask & ~correct_format_mask

    df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
    return df