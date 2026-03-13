import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from typing import Dict, Tuple, Set
from loguru import logger

# --------- Check mandatory ----------
@logger.catch
def is_empty(sr: ArrayLike = None, empty_value_list: ArrayLike| Dict| Tuple| Set = ["", None, "nan", "null", "NaN", np.nan, pd.NA]) -> pd.Series:
    """Return True if cell value is empty value else False."""
    mask: pd.Series = sr.isna()
    if empty_value_list:
        mask = mask | sr.isin(empty_value_list)

    return mask