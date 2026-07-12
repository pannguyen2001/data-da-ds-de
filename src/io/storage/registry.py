from src.common.constants import ResolveFileType
from src.io.storage.base import Storage
from src.io.storage.storage_parquet import ParquetStorage

_STORAGES: dict[ResolveFileType, type[Storage]] = {
    ResolveFileType.PARQUET: ParquetStorage
}
