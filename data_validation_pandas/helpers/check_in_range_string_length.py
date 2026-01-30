import pandas as pd
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# ---------- Check in range string length ----------

@logger.catch
def is_string_length_in_range(sr: pd.Series = None, lower_range: int = 0, upper_range: int = 0) -> pd.Series:
    """Resturn True if string is not in range, else False."""
    mask: pd.Series = sr.map(lambda x: lower_range <= len(x) <= upper_range)
    return mask

@validation_wrapper
def check_in_range_string_length(df: pd.DataFrame = None, column_name: str = "", length_range=Tuple[int, int]) -> Tuple[pd.Series, str]:
    """Return error message for each cell if string value is out of range, else none."""

    lower_range: int = length_range[0]
    upper_range: int = length_range[1]
    if lower_range > upper_range:
        lower_range, upper_range = upper_range, lower_range

    message: str = error_message["check_in_range_string_length"].format(column_name, length_range[0], length_range[1])

    empty_mask: pd.Series = is_empty(df[column_name])
    # Just check not empty cell
    # Assume that all are str
    not_in_range_mask: pd.Series = is_string_length_in_range(df[column_name], lower_range, upper_range)
    mask: pd.Series = ~empty_mask & ~not_in_range_mask

    return mask, message
