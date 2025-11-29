import pandas as pd
import numpy as np
from typing import Dict, List, Union, Any, Callable

class DataValidation:
    def __init__(
        self,
        df: pd.DataFrame,
        validation_config: Dict[str, Dict[str, Any]],
        ):
        self.df = df
        self.validation_config = validation_config
        if "result_detail" not in self.df.columns:
            self.df["result_detail"] = [set() for _ in range(self.df.shape[0])]
        self.validation_action_mapping = {
            "mandatory": self.check_mandatory,
            "datetime_format": self.check_datetime_format,
            "error_value": self.check_error_value,
            "refer_required": self.check_refer_required,
            "refer_value": self.check_refer_value,
            "non_existed_columns": self.check_existed_columns
        }
        self.error_messages = {
            "required": "[{}] Required field.",
            "error_value": "[{}] Value not in dropdown list.",
            "refer_required": "[{}] Required if '{}' is '{}'.",
            "refer_value": "[{}] Must be '{}' if '{}' is '{}'.",
            "datetime_format": "[{}] Datetime format must be YYYY-MM-DD.",
            "non_existed_columns": "[{}] Columns are not existed in dataframe."
        }

    def check_null(self, column_name: str = "") -> pd.Series:
        """Check each item of pd.Series is null/na or not

        Returns:
            pd.Series: a mask of pd.Series, contains True if item is null/na, otherwise False
        """

        return (self.df[column_name] == "") | (self.df[column_name].isna())

    def check_mandatory(self, **kwargs):
        """Check required column has empty value or not. If empty, add error message to result_detail"""

        column_name: str = kwargs.get("column_name")
        is_mandatory: bool = kwargs.get("is_mandatory")
        query_string: str = kwargs.get("query_string")

        message = self.error_messages["required"].format(column_name)
        mandatory_mask = self.check_null(column_name)

        if not is_mandatory:
            raise ValueError(f"[{self.check_mandatory.__name__}: {column_name}] Field 'is_mandatory' is required")

        if is_mandatory:
            if query_string:
                query_index = self.df.query(query_string).index
                query_mask = self.df.index.isin(query_index)
                mandatory_mask = query_mask & mandatory_mask

            self.df.loc[mandatory_mask, "result_detail"] = self.df.loc[mandatory_mask, "result_detail"].map(lambda x: x.union({message}))

    def check_datetime_format(self, **kwargs):
        """Check value of column is datetime or not. If not, add error message to result_detail"""

        column_name: str = kwargs.get("column_name")
        date_format: str = kwargs.get("format")
        query_string: str = kwargs.get("query_string")

        message = self.error_messages["datetime_format"].format(column_name)
        datetime_mask = (~self.check_null(column_name)) & (pd.to_datetime(self.df[column_name], format=date_format, errors="coerce").isna())

        if not date_format:
            raise ValueError(f"[{self.check_datetime_format.__name__}: {column_name}] Date_format is required")

        if query_string:
            query_index = self.df.query(query_string).index
            query_mask = self.df.index.isin(query_index)
            datetime_mask = datetime_mask & query_mask

        self.df.loc[datetime_mask, "result_detail"] = self.df.loc[datetime_mask, "result_detail"].map(lambda x: x.union({message}))

    def check_error_value(self, **kwargs):
        """Check value of column is in value_list or not. If not, add error message to result_detail"""

        column_name: str = kwargs.get("column_name")
        value_list: List = kwargs.get("value_list")
        query_string: str = kwargs.get("query_string")

        if not value_list:
            raise ValueError(f"[{self.check_error_value.__name__}: {column_name}] Value_list is required")

        message = self.error_messages["error_value"].format(column_name)
        value_mask = (~self.check_null(column_name)) & (~self.df[column_name].isin(value_list))

        if query_string:
            query_index = self.df.query(query_string).index
            query_mask = self.df.index.isin(query_index)
            value_mask = value_mask & query_mask

        self.df.loc[value_mask, "result_detail"] = self.df.loc[value_mask, "result_detail"].apply(lambda x: x.union({message}))

    def check_refer_required(self, **kwargs):
        """Check refer column has empty value or not. If empty, add error message to result_detail"""

        column_name: str = kwargs.get("column_name")
        refer_info: Dict = kwargs.get("refer_info")

        if not refer_info:
            raise ValueError(f"[{self.check_refer_required.__name__}: {column_name}] Must have refer info")

        for refer_column, refer_data in refer_info.items():
            refer_value: Any = refer_data.get("refer_value")
            query_string: str = refer_data.get("query_string")

            if not refer_column in self.df.columns:
                raise ValueError(f"[{self.check_refer_required.__name__}: {column_name}] {refer_column} not in dataframe columns.")

            if not refer_value:
                raise ValueError(f"[{self.check_refer_required.__name__}: {column_name}] {refer_column} must have refer value")

            if not query_string:
                raise ValueError(f"[{self.check_refer_required.__name__}: {column_name}] {refer_column} must have query string")

            query_index = self.df.query(query_string).index
            query_mask = self.df.index.isin(query_index)
            refer_mask = self.check_null(column_name) & query_mask

            message = self.error_messages["refer_required"].format(column_name, refer_column, refer_value)

            self.df.loc[refer_mask, "result_detail"] = self.df.loc[refer_mask, "result_detail"].map(lambda x: x.union({message}))

    def check_refer_value(self, **kwargs):
        """Check refer column has empty value or not. If empty, add error message to result_detail"""

        column_name: str = kwargs.get("column_name")
        refer_info: Dict = kwargs.get("refer_info")

        if not refer_info:
            raise ValueError(f"[{self.check_refer_value.__name__}: {column_name}] Must have refer value")

        for refer_column, refer_data in refer_info.items():
            if refer_column not in self.df.columns:
                raise ValueError(f"[{self.check_refer_value.__name__}: {column_name}] {refer_column} is not in dataframe columns")

            column_value: Any = refer_data.get("column_value")
            refer_value: Any = refer_data.get("refer_value")
            query_string: str = refer_data.get("query_string")

            if not column_value:
                raise ValueError(f"[{self.check_refer_value.__name__}: {column_name}] Must have column value")
            if not refer_value:
                raise ValueError(f"[{self.check_refer_value.__name__}: {column_name}] Must have refer value")
            if not query_string:
                raise ValueError(f"[{self.check_refer_value.__name__}: {column_name}] Must have query string")

            query_index = self.df.query(query_string).index
            query_mask = self.df.index.isin(query_index)
            refer_mask = ~self.check_null(column_name) & query_mask

            message = self.error_messages["refer_value"].format(
                column_name,
                column_value,
                refer_column,
                refer_value
                )

            self.df.loc[refer_mask, "result_detail"] = self.df.loc[refer_mask, "result_detail"].map(lambda x: x.union({message}))

    def check_existed_columns(self, **kwargs):
        """Check column name is existed in dataframe or not. If not, add error message to result_detail"""
        column_name_list: Union[List, str] = kwargs.get("column_name_list")
        if not column_name_list:
            raise ValueError(f"[{self.check_existed_columns.__name__}] Column_name_list is required")
        if isinstance(column_name_list, str):
            column_name_list = column_name_list.split(",")
            column_name_list = [column_name.strip() for column_name in column_name_list]

        non_existed_columns = set(column_name_list) - set(self.df.columns)
        message = self.error_messages["non_existed_columns"].format(", ".join(non_existed_columns))
        if len(non_existed_columns) > 0:
            self.df.loc[:, "result_detail"] = self.df.loc[:, "result_detail"].map(lambda x: x.union({message}))

    def run(self):
        """Run all validations across all configured columns"""

        for column_name, column_validation_config in self.validation_config.items():
            if not column_name:
                raise ValueError("column_name is required")
            if column_name not in self.df.columns:
                raise ValueError(f"{column_name} is not in dataframe")

            for action, config in column_validation_config.items():
                func = self.validation_action_mapping.get(action, None)
                if func:
                    func(column_name=column_name, **config)
                else:
                    raise ValueError(f"Invalid action: {action}")

        return self.df
