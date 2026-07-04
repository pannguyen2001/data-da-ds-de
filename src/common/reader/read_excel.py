from pathlib import Path
from typing import List, Union

import polars as pl
from pydantic.dataclasses import dataclass
from python_calamine import CalamineWorkbook

from src.common.reader.base import FileReader


@dataclass
class ExcelReader(FileReader):
    def validate(self, file_path: Path) -> None:
        super().validate(self.config.file_path)

        if self.config.options is None:
            raise ValueError(f"[{self.__class__.__name__}] options is required.")

        config_sheet_name: str = self.config.options.get("sheet_name", [])
        config_cols: Union[str, List[str]] = self.config.options.get("columns", [])

        if isinstance(config_cols, str):
            config_cols = [config_cols]

        workbook = CalamineWorkbook.from_path(self.config.file_path)
        sheet_names = workbook.sheet_names

        if config_sheet_name not in sheet_names:
            raise ValueError(
                f"[{self.__class__.__name__}] '{','.join(config_sheet_name)}' does not exist in file '{str(self.config.file_path)}'. Existing sheet: {', '.join(sheet_names)}."
            )

        sheet = workbook.get_sheet_by_name(config_sheet_name)
        sheet_data = sheet.to_python()
        cols = [str(col) for col in sheet_data[0] if col is not None and col]
        invalid_cols = set(config_cols) - set(cols)

        if invalid_cols:
            raise ValueError(
                f"[{self.__class__.__name__}] '{', '.join(invalid_cols)}' does not exist in sheet '{sheet}', file '{str(self.config.file_path)}'. Existing columns: {', '.join(cols)}."
            )

    def _do_load(self) -> pl.LazyFrame:
        """
        Read per sheet in excel file.
        Common settings:
            sheet_name=sheet_names,
            has_header=True,
            columns=columns,
            infer_schema_length=0,
        """

        return pl.read_excel(self.config.file_path, **self.config.options).lazy()
