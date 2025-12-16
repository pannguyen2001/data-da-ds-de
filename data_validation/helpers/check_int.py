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

# ---------- Check is int ----------
INT_TYPE = (int, np.integer)

@logger.catch
def is_int(sr: pd.Series) -> pd.Series:
    """Return True if each value cell is int or False if not."""
    return sr.map(lambda _: isinstance(_, INT_TYPE))

@logger.catch
def check_int(df: pd.DataFrame = None, column_name: str = "",
    ) -> pd.DataFrame:
    """Return error message if value is not int else no message."""

    logger.info(f"Check int for column: {column_name}")
    message: str = error_message["check_data_type"].format(column_name, "int")

    empty_check: pd.Series = is_empty(df[column_name])
    int_check: pd.Series = is_int(df[column_name])
    mask = ~empty_check & ~int_check

    df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
    logger.success(f"Complete checking int for column: {column_name}")

    return df