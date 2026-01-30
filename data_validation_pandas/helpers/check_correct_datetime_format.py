import pandas as pd
from typing import Tuple
from loguru import logger
from .is_empty import is_empty
from .validation_wrapper import validation_wrapper
from utils.constant import error_message

# ---------- Check datetime format ----------
@logger.catch
def is_correct_datetime_format(
    sr: pd.Series = None,
    input_format: str = "%Y-%m-%d"
    ) -> pd.Series:
    """Return True in each cell if can be converted to datetime follow format, else False."""
    return pd.to_datetime(sr, errors="coerce", format=input_format).notna()

@validation_wrapper
def check_correct_datetime_format(df: pd.DataFrame = None, column_name: str = "", datetime_format: str = "%Y-%m-%d") -> Tuple[pd.Series, str]:
    """Return error message if cell value is incorrect datetime format else no message. Ignore empty value."""

    message: str = error_message["check_correct_datetime_format"].format(column_name, datetime_format)

    empty_mask: pd.Series = is_empty(df[column_name])
    correct_format_mask: pd.Series = is_correct_datetime_format(df[column_name], datetime_format)
    # Invalid value is:
    # - Not empty
    # - Wrong input format
    mask: pd.Series = ~empty_mask & ~correct_format_mask

    return mask, message

# @logger.catch
# def check_correct_datetime_format(df: pd.DataFrame = None, column_name: str = "", datetime_format: str = "%Y-%m-%d") -> pd.DataFrame:
#     """Return error message if cell value is incorrect datetime format else no message. Ignore empty value."""

#     logger.info(f"Check correct datetime format for column: {column_name}")
#     message: str = error_message["check_correct_datetime_format"].format(column_name, datetime_format)

#     empty_mask: pd.Series = is_empty(df[column_name])
#     correct_format_mask: pd.Series = is_correct_datetime_format(df[column_name], datetime_format)
#     # Invalid value is:
#     # - Not empty
#     # - Wrong input format
#     mask: pd.Series = ~empty_mask & ~correct_format_mask

#     if mask.any():
#         df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
#         incorrect_format_index: pd.Series = df.loc[mask, column_name].index + 2
#         sample_indexes: pd.Series = incorrect_format_index[:5].tolist() if incorrect_format_index.shape[0] > 5 else incorrect_format_index.tolist()
#         logger.warning(f"[Incorrect datetime format '{datetime_format}'] {len(incorrect_format_index)}/{df.shape[0]} values. Excel index example: {sample_indexes}.")
#     else:
#         logger.success("All values are correct datetime format.")

#     # logger.success(f"Complete checking correct datetime format for column: {column_name}.")

#     return df
