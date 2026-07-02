# import sys
# import os
# print(sys.version)

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# print(sys.path)
from pathlib import Path

from src.pipeline.engine import PipelineEngine
from src.common.logger import logger

logger.info("Start pipeline...")

pipeline = PipelineEngine({
    "source_config_path": Path("/home/user/data-da-ds-de/configs/source.yaml"),
    "options": {
        "encoding": "utf-8",
        "errors": "raise",
        "mode": "r"
    }
})
pipeline.run()

logger.info("Pipeline completed.")