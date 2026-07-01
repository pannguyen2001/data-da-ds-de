import yaml
from pydantic.dataclasses import dataclass

from common.strategies.loader.base import FileLoader


@dataclass
class ReadYAMLFileStrategy(FileLoader):
    def _do_load(self) -> list:
        with open(self.config.file_path, **self.config.options) as file:
            data = yaml.safe_load(file)
        return data
