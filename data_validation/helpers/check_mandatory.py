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

# --------- Check mandatory ----------

@logger.catch
def check_mandatory(df: pd.DataFrame = None, column_name: str = "", empty_value_list: list = None) -> pd.DataFrame:
    """Return error message if value cell is empty, else none."""

    logger.info(f"Check mandatory for column: {column_name}")
    message: str = error_message["check_mandatory"].format(column_name)
    empty_result: pd.Series = is_empty(df[column_name])

    df.loc[empty_result, "validation_result"] = df.loc[empty_result, "validation_result"].map(add_message_function(message))
    logger.success(f"Complete checking mandatory for column: {column_name}")

    return df