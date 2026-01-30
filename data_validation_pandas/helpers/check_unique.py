import pandas as pd
from loguru import logger
from typing import Tuple
from .is_empty import is_empty
from utils.constant import error_message
from .validation_wrapper import validation_wrapper

# --------- Check unique ----------
@logger.catch
def not_unique(series: pd.Series = None) -> pd.Series:
    """Return True if value is not unique else False."""
    return series.duplicated(keep=False) # keep=False, all rows that are part of a duplicate group are flagged as True. Unique rows are marked as False. So if duplicated, return False => compare with False => return True

@validation_wrapper
def check_unique(df: pd.DataFrame, column_name: str) -> Tuple[pd.Series, str]:
    """Return True if value is not unique else False."""
    message: str = error_message["check_unique"].format(column_name)

    empty_check: pd.Series = is_empty(df[column_name])
    unique_check: pd.Series = not_unique(df[column_name])
    mask = ~empty_check & unique_check

    return mask, message

# @logger.catch
# def check_unique(df: pd.DataFrame = None, column_name: str = "",
#     ) -> pd.DataFrame:
#     """Return error message if value is not unique else no message."""

#     logger.info(f"Check unique for column: {column_name}")
#     message: str = error_message["check_data_type"].format(column_name, "unique")

#     empty_check: pd.Series = is_empty(df[column_name])
#     unique_check: pd.Series = not_unique(df[column_name])
#     mask = ~empty_check & unique_check

#     if mask.any():
#         df.loc[mask, "validation_result"] = df.loc[mask, "validation_result"].map(add_message_function(message))
#         not_unique_index: pd.Series = df.loc[mask, column_name].index + 2
#         sample_indexes: pd.Series = not_unique_index[:5].tolist() if not_unique_index.shape[0] > 5 else not_unique_index.tolist()
#         logger.warning(f"[Not unique] {len(not_unique_index)}/{df.shape[0]} values. Excel index example: {sample_indexes}.")
#     else:
#         logger.info("All values are unique.")

#     # logger.success(f"Complete checking unique for column: {column_name}.")

#     return df