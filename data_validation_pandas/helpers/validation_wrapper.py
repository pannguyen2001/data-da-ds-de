import pandas as pd
from functools import wraps
from typing import Callable, Tuple
from loguru import logger
from utils.constant import  add_message_function


def validation_wrapper(validation_function: Callable[..., Tuple[pd.Series, str]]) -> Callable:
    @logger.catch
    @wraps(validation_function)
    def wrapper(
        df: pd.DataFrame = None,
        column_name: str = "",
        *args,
        **kwargs
    ) -> pd.DataFrame:
        logger.info(f"Running validation rule: '{validation_function.__name__}' for column: '{column_name}'.")

        if df is None or df.empty:
            logger.error("Dataframe is empty or having error.")
            return df

        if df is not None and "validation_result" not in df.columns:
            df["validation_result"] = [set() for _ in range(df.shape[0])]

        # output is validation_result series
        result, message = validation_function(
            df,
            column_name,
            *args,
            **kwargs
        )
        # keep
        if not result.any():
            logger.info("No issue found.")
            return df

        # This will be added to self.validation_result in class BaseValidation
        df.loc[result, "validation_result"] = df.loc[result, "validation_result"].map(add_message_function(message))
        result_index: pd.Series = df.loc[result, column_name].index + 2
        # keep
        sample_indexes: pd.Series = result_index[:5].tolist() if result_index.shape[0] > 5 else result_index.tolist()

        rule_name = validation_function.__name__
        logger.warning(f"[{rule_name}][{column_name}] {len(result_index)}/{df.shape[0]} invalid values. Excel index example: {sample_indexes}.")

        # Add processing result here

        # Result is validation_result mask boolean series

        return df

    return wrapper

