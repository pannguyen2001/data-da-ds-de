from src.common.constants import ResolveFileType
from .load_yaml import LoadYaml

_LOADERS = {
    ResolveFileType.YAML: LoadYaml,
}