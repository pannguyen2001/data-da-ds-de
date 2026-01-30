import pandas as pd
import numpy as np
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# ---------- Check is int ----------
INT_TYPE = (int, np.integer)

@logger.catch
def is_int(sr: pd.Series) -> pd.Series:
    """Return True if each value cell is int or False if not."""
    return sr.map(lambda x: isinstance(x, INT_TYPE))

@validation_wrapper
def check_int(df: pd.DataFrame = None, column_name: str = "") -> Tuple[pd.Series, str]:
    """Return error message if value is not int else no message."""

    message: str = error_message["check_data_type"].format(column_name, "int")

    empty_check: pd.Series = is_empty(df[column_name])
    int_check: pd.Series = is_int(df[column_name])
    mask = ~empty_check & ~int_check

    return mask, message