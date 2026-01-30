import pandas as pd
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# ---------- Check in range datetime ----------
@logger.catch
def is_in_range_datetime(sr: pd.Series, range: Tuple[str, any]) -> pd.Series:
    "Return pd.Series, contains value True if cell value is in rage else False."
    return (range[0] <= sr) & (sr <= range[1])

@validation_wrapper
def check_in_range_datetime(
    df: pd.DataFrame = None,
    column_name: str = "",
    range: Tuple[str, any] = ("", ""),
    datetime_format: str = "%Y-%m-%d"
    ) -> Tuple[pd.Series, str]:
    """Return True if datetime value in cell is not in range else False. Ignore empty values."""

    message: str = error_message["check_in_range_datetime"].format(column_name, range[0], range[1])

    lower_range = pd.to_datetime(range[0], format=datetime_format)
    upper_range = pd.to_datetime(range[1], format=datetime_format)
    if pd.to_datetime(range[0]) > pd.to_datetime(range[1]):
        lower_range, upper_range = upper_range, lower_range

    empty_mask: pd.Series = is_empty(df[column_name])
    in_range_mask: pd.Series = is_in_range_datetime(df[column_name], range)
    mask: pd.Series = ~empty_mask & ~in_range_mask

    return mask, message