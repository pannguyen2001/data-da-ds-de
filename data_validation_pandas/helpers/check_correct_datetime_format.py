import pandas as pd
from typing import Tuple
from loguru import logger
from .is_empty import is_empty
from .validation_wrapper import validation_wrapper
from utils.constant import error_message

# ---------- Check datetime format ----------
@logger.catch
def is_correct_datetime_format(
    sr: pd.Series = None,
    input_format: str = "%Y-%m-%d"
    ) -> pd.Series:
    """Return True in each cell if can be converted to datetime follow format, else False."""
    return pd.to_datetime(sr, errors="coerce", format=input_format).notna()

@validation_wrapper
def check_correct_datetime_format(df: pd.DataFrame = None, column_name: str = "", datetime_format: str = "%Y-%m-%d") -> Tuple[pd.Series, str]:
    """Return True if cell value is incorrect datetime format else False. Ignore empty value."""

    message: str = error_message["check_correct_datetime_format"].format(column_name, datetime_format)

    empty_mask: pd.Series = is_empty(df[column_name])
    correct_format_mask: pd.Series = is_correct_datetime_format(df[column_name], datetime_format)
    # Invalid value is:
    # - Not empty
    # - Wrong input format
    mask: pd.Series = ~empty_mask & ~correct_format_mask

    return mask, message