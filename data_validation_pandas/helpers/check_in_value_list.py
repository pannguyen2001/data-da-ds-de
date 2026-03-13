import pandas as pd
import numpy as np
from typing import Tuple, List
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# --------- Check mandatory ----------

@validation_wrapper
def check_in_value_list(df: pd.DataFrame = None, column_name: str = "", value_list: List = None) -> Tuple[pd.Series, str]:
    """Return True if value cell is not in value list else False. Ignore empty value."""
    if not value_list:
        raise ValueError("value_list is required")
        return

    message: str = error_message["check_in_value_list"].format(column_name, value_list)

    is_empty_mask: pd.Series = is_empty(df[column_name])
    in_value_list_mask: pd.Series = df[column_name].isin(value_list)
    mask: pd.Series = ~is_empty_mask & ~in_value_list_mask

    return mask, message