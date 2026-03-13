import pandas as pd
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper
from .check_correct_datetime_format import check_correct_datetime_format

# ---------- Check in range datetime ----------
@logger.catch
def is_in_range_datetime(sr: pd.Series, datetime_range: Tuple[str, any]) -> pd.Series:
    "Return pd.Series, contains value True if cell value is in rage else False."
    return (datetime_range[0] <= sr) & (sr <= datetime_range[1])

@validation_wrapper
def check_in_range_datetime(
    df: pd.DataFrame = None,
    column_name: str = "",
    datetime_range: Tuple[str, str] = ("", ""),
    datetime_format: str = "%Y-%m-%d"
    ) -> Tuple[pd.Series, str]:
    """Return True if datetime value in cell is not in range else False. Ignore empty values."""

    message: str = error_message["check_in_range_datetime"].format(column_name, datetime_range[0], datetime_range[1])

    lower_range = pd.to_datetime(datetime_range[0], format=datetime_format)
    upper_range = pd.to_datetime(datetime_range[1], format=datetime_format)
    if lower_range > upper_range:
        lower_range, upper_range = upper_range, lower_range

    empty_mask: pd.Series = is_empty(df[column_name])

    correct_format_mask: pd.Series = pd.to_datetime(df[column_name], format=datetime_format, errors="coerce").notna()
    # Invalid value is:
    # - Not empty
    # - Correct input format
    # - Out of range
    in_range_datetime_mask: pd.Series = is_in_range_datetime(pd.to_datetime(df[column_name], format=datetime_format, errors="coerce"), (lower_range, upper_range))
    mask: pd.Series = ~empty_mask & correct_format_mask & ~in_range_datetime_mask

    return mask, message