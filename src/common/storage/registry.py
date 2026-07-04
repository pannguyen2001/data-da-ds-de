from src.common.constants import ResolveFileType
from src.common.storage.base import Storage
from src.common.storage.storage_parquet import ParquetStorage

_STORAGES: dict[ResolveFileType, type[Storage]] = {
    ResolveFileType.PARQUET: ParquetStorage
}
