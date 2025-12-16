import datetime
import pandas as pd
import numpy as np
import os
import sys
import pytz
from numpy.typing import ArrayLike, DTypeLike, NDArray
from typing import Sequence, List, Dict, Tuple, Set, Any, Union, Optional, Annotated, Callable, Literal, TypeVar
from loguru import logger
from utils.constant import error_message, add_message_function

# --------- Check mandatory ----------
@logger.catch
def is_empty(sr: ArrayLike = None, empty_value_list: ArrayLike| Dict|Tuple|Set = None) -> pd.Series:
    """Return True if cell value is empty value else False."""
    mask: pd.Series = sr.isna()
    if empty_value_list:
        mask = mask | sr.isin(empty_value_list)
    return mask