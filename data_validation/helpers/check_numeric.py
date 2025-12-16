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

# ---------- Check is numeric ----------
@logger.catch
def is_numeric(sr: pd.Series) -> pd.Series:
    """Return True if each value cell is numeric or False if not."""
    return pd.to_numeric(sr, errors="coerce").notna()

@logger.catch
def check_numeric(df: pd.DataFrame = None, column_name: str = "",
    ) -> pd.DataFrame:
    """Return error message if value is not numeric else no message."""

    logger.info(f"Check numeric for column: {column_name}")
    message: str = error_message["check_data_type"].format(column_name, "number")

    empty_check: pd.Series = is_empty(df[column_name])
    numeric_check: pd.Series = is_numeric(df[column_name])
    mask = ~empty_check & ~numeric_check

    df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
    logger.success(f"Complete checking numeric for column: {column_name}")

    return df