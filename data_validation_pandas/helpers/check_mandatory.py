import pandas as pd
import numpy as np
from typing import Tuple, List
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# --------- Check mandatory ----------

@validation_wrapper
def check_mandatory(df: pd.DataFrame = None, column_name: str = "", empty_value_list: List = ["", None, "nan", "null", "NaN", np.nan, pd.NA]) -> Tuple[pd.Series, str]:
    """Return True if value cell is empty else False."""
    # if df is None or df.empty:
    #     logger.error("Dataframe is empty or having error.")
    #     return df

    message: str = error_message["check_mandatory"].format(column_name)

    mask: pd.Series = is_empty(df[column_name], empty_value_list)

    return mask, message