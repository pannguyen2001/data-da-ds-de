from src.common.constants import ResolveFileType
from src.io.loader.base import FileLoader

from .load_yaml import LoadYaml

_LOADERS: dict[ResolveFileType, type[FileLoader]] = {
    ResolveFileType.YAML: LoadYaml,
}
