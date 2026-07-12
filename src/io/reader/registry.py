from src.common.constants import ResolveFileType
from src.io.reader.base import FileReader

from .read_csv import CsvReader
from .read_excel import ExcelReader
from .read_json import JsonReader
from .read_parquet import ParquetReader
from .read_sql import SqlReader

_READERS: dict[ResolveFileType, type[FileReader]] = {
    ResolveFileType.CSV: CsvReader,
    ResolveFileType.EXCEL: ExcelReader,
    ResolveFileType.JSON: JsonReader,
    ResolveFileType.PARQUET: ParquetReader,
    ResolveFileType.SQL: SqlReader,
}
