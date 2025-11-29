# import sqlite3
# # from helpers import logger_wrapper
# from helpers.logger import other_common_logger
# from utils import test_db_file_path
# from helpers import connect_db, close_db, excel_to_sql, csv_to_sql, read_db

# from functions import check_config

# check_config("configs/data_source.xlsx")

# Check file data_source_config.xlsx is exist or not, if not, log error and end program.
# from helpers import check_file_exist

# check_file_exist("configs/test/data_source.xlsx")

# Connect to database

import pandas as pd
import numpy as np
from helpers.logger import common_phase_logger

data_validation_logger = common_phase_logger.bind(sub_phase="data_validation")

df: pd.DataFrame = pd.DataFrame(
    {
        "name": ["John", "Anna", "Peter", "Linda", "May", np.nan],
        "sex": ["M", "F", "M", "FF", "F", np.nan],
        "age": [10, 18, 35, np.nan, "40", np.nan],
        "is_adult": [True, True, True, True, True, "False"],
        "datetime": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05 00:00:00", np.nan],
        "multiple_values": ["A,B", "C,D", "A,B", "A,B", "I,J", np.nan],
    }
).convert_dtypes()

data_pre_processing: dict = {
    "drop_columns": ["sex"],
    "rename_columns": {
        "name": "full_name",
    },
    "split_data": {
        "multiple_values": ","
    },
    "mapping_value": {
        "is_adult": {
            True: "true",
            False: "false",
            None: "null"
        }
    }
}

validation_config: dict = {
    "check_mandatory": [
        "name",
        "sex",
        "is_adult",
        "datetime",
        "multiple_values"
        ],
    "check_invalid_value": {
        "sex": {
            "type": "single_value",
            "value_list": ["M", "F"],
            "separator": None,
            },
        "multiple_values": {
            "type": "multi_value",
            "value_list": ["A", "B", "C", "D"],
            "separator": ",",
        }
        # {"type": "single_value", "value_list": ["M", "F"], "separator": None} | {"type": "multi_value", "value_list": ["M", "F"], "separator": ","}
    },
    "check_datetime_format": {
        "datetime": "%Y-%m-%d"
    },
    "check_data_type": {
        "name": "str",
        "sex": "str",
        "age": "int|int16|int32|int64",
        "is_adult": "bool",
        "datetime": "str"
    },
    "mapping_value": {
        "is_adult": {
            True: "true",
            False: "false",
            None: "null"
        }
    },
    "check_refer_required": {
        "age": ["is_adult"] # mask: empty check => then apply qcheck refered mask for each column in list
    },
    "check_invalid_refer_value": {
        "age": {
            "correct_values": [0],
            "query_str": "(`is_adult` == True) and (`multiple_values`.isin(['A', 'B']))",
        }
    }
}
# incorrect format
# incorrect data type
# just check if not empty, except check mandaory

data_mapping: dict = {
    True: "True",
    False: "False",
    None: "null",
}

class DataPreProcessing:
    def __init__(
        self,
        df: pd.DataFrame,
        config: dict = None,
        result_columns_name: str = "result_report",
    ) -> None:
        self.df: pd.DataFrame = df
        self.config: dict = config
        self.result_columns_name: str = result_columns_name


class DataValidation:
    def __init__(
        self,
        df: pd.DataFrame,
        extra_na_values: list | set | np.ndarray = None,
        config: dict = None,
        result_columns_name: str = "result_report",
    ) -> None:
        self.df: pd.DataFrame = df
        self.df_empty_value_check: pd.DataFrame = pd.DataFrame()
        self.extra_na_values: list | set | np.ndarray = extra_na_values
        self.config: dict = config
        self.result_columns_name: str = result_columns_name
        if not self.result_columns_name:
            self.result_columns_name: str = "result_report"
        self.df[self.result_columns_name] = [set() for _ in range(df.shape[0])]
        self.validation_function_mapping: dict = {
            "check_mandatory": self.check_mandatory,
            "check_invalid_value": self.check_invalid_value,
            "check_datetime_format": self.check_datetime_format,
            "check_data_type": self.check_data_type,
            "mapping_value": self.mapping_value,
            "check_refer_required": self.check_refer_required,
            "check_invalid_refer_value": self.check_invalid_refer_value,
        }
        self.error_message_format: dict = {
            "check_mandatory": "[{}] Required field.",
            "check_invalid_value": "[{}] Value must be one of these: '{}'.",
            "check_refer_required": "[{}] Required when '{}' have/has value.",
            "check_invalid_refer_value": "[{}] Refered value must be one of these: '{}'.",
            "check_invalid_data_type": "[{}] Data type must be one of these: '{}'.",
            "check_datetime_format": "[{}] Format must be: '{}'.",
        }
        self.data_mapping: dict = {
            True: "true",
            False: "false",
            None: "null",
        }

    @data_validation_logger.catch
    def check_empty_value(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """Check column contains empty value or not."""

        self.df_empty_value_check: pd.DataFrame = self.df[self.df.columns[:-1]].apply(
            lambda x: x.isna()
            | (self.extra_na_values is not None and x.isin(self.extra_na_values)),
            axis=1,
        )

    @data_validation_logger.catch
    def check_mandatory(self, column_list: list = None) -> None:
        if not column_list or column_list == ["all"]:
            column_list = self.df.columns[:-1]

        incorrect_column_list: set = set(column_list) - set(self.df.columns)
        if len(incorrect_column_list) > 0:
            raise ValueError(
                f"[{self.check_mandatory.__name__}] column_list contains column not in df: {incorrect_column_list}."
            )

        for col in column_list:
            mask: pd.Series = self.df_empty_value_check[col]
            self.df.loc[mask, self.result_columns_name] = self.df.loc[mask, self.result_columns_name].map(
                lambda _: _.union({self.error_message_format["check_mandatory"].format(col)})
            )
        return self.df

    @data_validation_logger.catch
    def check_invalid_value(self, config: dict = None) -> None:

        for col, config_values in config.items():
            check_type: dict = config_values.get("type", None)
            if not check_type:
                raise ValueError(f"[{self.check_invalid_value.__name__}] type is required or incorrect.")
            if check_type not in ["single_value", "multi_value"]:
                raise ValueError(f"[{self.check_invalid_value.__name__}] type is required or incorrect.")

            value_list: list = config_values.get("value_list", None)
            if not value_list:
                raise ValueError(f"[{self.check_invalid_value.__name__}] value_list is required or incorrect.")

            separator: str = config_values.get("separator", None)
            if check_type == "multi_value" and separator is None:
                raise ValueError(f"[{self.check_invalid_value.__name__}] separator is required or incorrect")

            mask: pd.Series = ~self.df_empty_value_check[col]
            if check_type == "multi_value":
                pre_processing_col: pd.Series = self.df[col].map(lambda x: [_.strip() for _ in x.split(separator)] if pd.notna(x) else [])
                mask &= pre_processing_col.map(lambda x: len(set(x) - set(value_list)) > 0)
            else:
                mask &= ~self.df[col].isin(value_list)

            self.df.loc[mask, self.result_columns_name] = self.df.loc[mask, self.result_columns_name].map(lambda x: x.union({self.error_message_format["check_invalid_value"].format(col, ", ".join(value_list))}))
        return self.df

    @data_validation_logger.catch
    def check_datetime_format(self, config: dict = None) -> None:
        for col, format_value in config.items():
            mask: pd.Series = ~self.df_empty_value_check[col] & self.df[col].map(lambda x: pd.to_datetime(x, format=format_value, errors="coerce")).isna()
            self.df.loc[mask, self.result_columns_name] = self.df.loc[mask, self.result_columns_name].map(lambda x: x.union({self.error_message_format["check_datetime_format"].format(col, format_value)}))
        return self.df

    @data_validation_logger.catch
    def check_data_type(self, config: dict = None) -> None:
        for col, data_type in config.items():
            data_type_list: list = data_type.split("|")
            mask: pd.Series = (~self.df_empty_value_check[col]) & self.df[col].map(lambda x: type(x).__name__ not in data_type_list)
            self.df.loc[mask, self.result_columns_name] = self.df.loc[mask, self.result_columns_name].map(lambda x: x.union({self.error_message_format["check_invalid_data_type"].format(col, ", ".join(data_type_list))}))
        return self.df

    @data_validation_logger.catch
    def mapping_value(self, config: dict = None) -> None:
        for col, mapping_value in config.items():
            mask: pd.Series = (~self.df_empty_value_check[col]) & (self.df[col].isin(mapping_value.keys()))
            self.df.loc[mask, col] = self.df.loc[mask, col].map(lambda x: mapping_value.get(x, x))
        return self.df

    def check_refer_required(self, config: dict = None) -> None:
        for col, refered_columns in config.items():
            mask: pd.Series = self.df_empty_value_check[col]
            for refered_column in refered_columns:
                mask &= ~self.df_empty_value_check[refered_column]
            self.df.loc[mask, self.result_columns_name] = self.df.loc[mask, self.result_columns_name].map(lambda x: x.union({self.error_message_format["check_refer_required"].format(col, ", ".join(refered_columns))}))
        return self.df

    @data_validation_logger.catch
    def check_invalid_refer_value(self, config: dict = None) -> None:
        for col, config_values in config.items():
            empty_mask: pd.Series = ~self.df_empty_value_check[col]
            correct_values: list = config_values.get("correct_values", None)
            if not correct_values:
                raise ValueError(f"[{self.check_invalid_refer_value.__name__}] correct_value is required or incorrect.")
            correct_values = [str(_) for _ in correct_values]

            query_str: str = config_values.get("query_str", None)
            if not query_str:
                raise ValueError(f"[{self.check_invalid_refer_value.__name__}] query is required or incorrect.")

            query_result: pd.Series = self.df.query(query_str).index
            query_mask = self.df.index.isin(query_result)
            query_data = self.df.loc[query_mask & empty_mask, col].index
            final= self.df.loc[query_data, col].isin(correct_values).index
            mask: pd.Series = ~self.df[col].index.isin(final)
            self.df.loc[mask, self.result_columns_name] = self.df.loc[mask, self.result_columns_name].map(lambda x: x.union({self.error_message_format["check_invalid_refer_value"].format(col, ", ".join(correct_values))}))
        return self.df


    @data_validation_logger.catch
    def run(self) -> None:
        data_validation_logger.info("Start validate data.")
        if self.df is None or self.df.empty:
            raise ValueError(f"[{self.run.__name__}] df is empty.")
        if not self.config:
            raise ValueError(f"[{self.run.__name__}] config is empty.")
        if not (
            isinstance(self.extra_na_values, list)
            or isinstance(self.extra_na_values, set)
            or isinstance(self.extra_na_values, np.ndarray)
        ):
            raise ValueError(
                f"[{self.check_empty_value.__name__}] extra_na_values must be a list, set or np.ndarray."
            )
        self.check_empty_value()
        for validation_type_name, validation_type_config in self.config.items():
            data_validation_logger.info(f"{validation_type_name = }, {validation_type_config = }")
            if not validation_type_config:
                raise ValueError(f"[{self.run.__name__}] {validation_type_name} config is empty.")
            self.validation_function_mapping[validation_type_name](validation_type_config)

        self.df[self.result_columns_name] = self.df[self.result_columns_name].map(lambda x: "\n".join(x))

        data_validation_logger.success("Complete validate data.")
        return self.df

validated_df: pd.DataFrame = DataValidation(df, [""], validation_config).run()

for index, row in df["result_report"].items():
    data_validation_logger.info(f"{index = }, {row = }")


logger_options: dict = data_validation_logger.__dict__["_options"][-1]
logger_options_str: str = "_".join(logger_options.values())
from utils.constants import report_folder
df.to_csv(f"{report_folder}/{logger_options_str}.csv")
