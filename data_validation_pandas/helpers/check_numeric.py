import pandas as pd
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# ---------- Check is numeric ----------
@logger.catch
def is_numeric(sr: pd.Series) -> pd.Series:
    """Return True if each value cell is numeric or False if not."""
    return pd.to_numeric(sr, errors="coerce").notna()

@validation_wrapper
def check_numeric(df: pd.DataFrame = None, column_name: str = "") -> Tuple[pd.Series, str]:
    """Return True if value is not numeric else False."""

    message: str = error_message["check_data_type"].format(column_name, "number")

    empty_check: pd.Series = is_empty(df[column_name])
    numeric_check: pd.Series = is_numeric(df[column_name])
    mask = ~empty_check & ~numeric_check

    return mask, message