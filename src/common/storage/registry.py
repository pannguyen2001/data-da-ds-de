from src.common.storage.storage_parquet import ParquetStorage
from src.common.constants import ResolveFileType

_STORAGES = {
    ResolveFileType.PARQUET: ParquetStorage
}