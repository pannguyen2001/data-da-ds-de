import pandas as pd
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# ---------- Check numeric range ----------
@validation_wrapper
def check_in_range_numeric(
    df: pd.DataFrame = None,
    column_name: str = "",
    input_range: Tuple[int | float, int | float] = (0, 0),
) -> Tuple[pd.Series, str]:
    """Return error message if cell value is not in range, else no message. Ignore empty value ro not numeric values."""

    message: str = error_message["check_in_range_numeric"].format(column_name, input_range[0], input_range[1])

    if input_range[0] > input_range[1]:
        input_range = (input_range[1], input_range[0])

    # values considered "empty"
    empty_mask: pd.Series = is_empty(df[column_name])
    # convert to numeric; non-numeric → NaN
    numeric_col = pd.to_numeric(df[column_name], errors="coerce")
    # non-numeric --> NaN --> will be ignored
    non_numeric_mask = numeric_col.isna() & (~empty_mask)
    # check numeric values in range
    range_mask = numeric_col.between(input_range[0], input_range[1], inclusive="both")
    # invalid only if:
    #   - numeric
    #   - NOT empty
    #   - NOT in range
    invalid_mask = (~range_mask) & (~empty_mask) & (~non_numeric_mask)

    return invalid_mask, message
