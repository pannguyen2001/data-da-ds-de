from src.pipeline.task.base import BaseTask
from src.pipeline.task.build_io_config import BuildIOConfigTask
from src.pipeline.task.check_source import CheckSourceTask
from src.pipeline.task.preprocess_source import PreprocessSourceTask
from src.pipeline.task.storage import StorageTask


_TASKS: dict[str, type[BaseTask]] = {
    BuildIOConfigTask.__name__: BuildIOConfigTask,
    CheckSourceTask.__name__: CheckSourceTask,
    PreprocessSourceTask.__name__: PreprocessSourceTask,
    StorageTask.__name__: StorageTask,
}