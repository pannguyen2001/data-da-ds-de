import pandas as pd
import numpy as np
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

    if mask.any():
        df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
        not_int_values: pd.Series = df.loc[mask, column_name].index + 2
        sample_indexes: pd.Series = not_int_values[:5].tolist() if not_int_values.shape[0] > 5 else not_int_values.tolist()
        logger.warning(f"[Not type int] {len(not_int_values)}/{df.shape[0]} values. Excel index example: {sample_indexes}.")
    else:
        logger.success("All values are int.")

    # logger.success(f"Complete checking int for column: {column_name}.")

    return df