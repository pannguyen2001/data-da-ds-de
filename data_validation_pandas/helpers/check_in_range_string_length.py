import pandas as pd
import numpy as np
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message, add_message_function

# ---------- Check in range string length ----------

@logger.catch
def is_string_length_in_range(sr: pd.Series = None, lower_range: int = 0, upper_range: int = 0) -> pd.Series:
    """Resturn True if string is not in range, else False."""
    mask: pd.Series = sr.map(lambda _: lower_range <= len(_) <= upper_range)
    return mask

@logger.catch
def check_in_range_string_length(df: pd.DataFrame = None, column_name: str = "", length_range=Tuple[int, int]) -> pd.DataFrame:
    """Return error message for each cell if string value is out of range, else none."""

    logger.info(f"Check in range string length for column: {column_name}")
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

    if mask.any():
        df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
        not_in_range_index: pd.Series = df.loc[mask, column_name].index + 2
        sample_indexes: pd.Series = not_in_range_index[:5].tolist() if not_in_range_index.shape[0] > 5 else not_in_range_index.tolist()
        logger.warning(f"[Out of range string length] {len(not_in_range_index)}/{df.shape[0]} values. Excel index example: {sample_indexes}.")
    else:
        logger.success("All values are in range.")

    # logger.success(f"Complete checking in range string length for column: {column_name}.")

    return df
