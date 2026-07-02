from src.common.constants import ResolveFileType
from .read_csv import CsvReader
from .read_excel import ExcelReader
from .read_json import JsonReader
from .read_parquet import ParquetReader
from .read_sql import SqlReader

_READERS = {
    ResolveFileType.CSV: CsvReader,
    ResolveFileType.EXCEL: ExcelReader,
    ResolveFileType.JSON: JsonReader,
    ResolveFileType.PARQUET: ParquetReader,
    ResolveFileType.SQL: SqlReader,
}