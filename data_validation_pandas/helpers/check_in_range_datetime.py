import pandas as pd
import numpy as np
from typing import Tuple
from loguru import logger
from .is_empty import is_empty
from utils.constant import error_message, add_message_function

# ---------- Check in range datetime ----------
@logger.catch
def is_in_range_datetime(sr: pd.Series, range: Tuple[str, any]) -> pd.Series:
    "Return pd.Series, contains value True if cell value is in rage else False."
    return (range[0] <= sr) & (sr <= range[1])

@logger.catch
def check_in_range_datetime(
    df: pd.DataFrame = None,
    column_name: str = "",
    range: Tuple[str, any] = ("", ""),
    datetime_format: str = "%Y-%m-%d"
    ) -> pd.DataFrame:
    """Return error message if datetime value in cell is not in range, else no message. Ignore empty values."""

    logger.info(f"Check in range datetime for column: {column_name}")
    message: str = error_message["check_in_range_datetime"].format(column_name, range[0], range[1])
    sr_datetime: pd.Series = pd.to_datetime(df[column_name], errors="coerce", format=datetime_format)
    lower_range = pd.to_datetime(range[0], format=datetime_format)
    upper_range = pd.to_datetime(range[1], format=datetime_format)
    if pd.to_datetime(range[0]) > pd.to_datetime(range[1]):
        lower_range, upper_range = upper_range, lower_range

    empty_mask: pd.Series = is_empty(df[column_name])
    in_range_mask: pd.Series = is_in_range_datetime(df[column_name], range)
    mask: pd.Series = ~empty_mask & ~in_range_mask

    if mask.any():
        df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
        incorrect_format_index: pd.Series = df.loc[mask, column_name].index + 2
        sample_indexes: pd.Series = incorrect_format_index[:5].tolist() if incorrect_format_index.shape[0] > 5 else incorrect_format_index.tolist()
        logger.warning(f"[Out of range datetime] {len(incorrect_format_index)}/{df.shape[0]} values. Excel index example: {sample_indexes}.")
    else:
        logger.success("All values are in range datetime.")

    # logger.success(f"Complete checking in range datetime for column: {column_name}.")

    return df