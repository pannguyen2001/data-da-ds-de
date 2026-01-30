import pandas as pd
import numpy as np
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

    if empty_result.any():
        df.loc[empty_result, "validation_result"] = df.loc[empty_result,"validation_result"].map(add_message_function(message))
        empty_values_index: pd.Series = df.loc[empty_result, column_name].index + 2
        sample_indexes: pd.Series = empty_values_index[:5].tolist() if empty_values_index.shape[0] > 5 else empty_values_index.tolist()
        logger.warning(f"[Empty] {len(empty_values_index)}/{df.shape[0]} values. Excel index example: {sample_indexes}.")
    else:
        logger.info("All values are not empty.")

    # logger.success(f"Complete checking mandatory for column: {column_name}.")

    return df
