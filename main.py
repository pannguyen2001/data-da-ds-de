# import sys
# import os
# print(sys.version)

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# print(sys.path)
from pathlib import Path
from typing import Any

from src.pipeline.engine import PipelineEngine
from src.common.logger import logger
from src.common.cleanup_file_or_folder import cleanup_file_or_folder
from src.common.constants import ResolveFileType


def main(setup: dict[str, Any]):
    logger.info("Start pipeline...")

    pipeline = PipelineEngine(setup)
    pipeline.run()

    logger.info("Pipeline completed.")


if __name__ == "__main__":
    setup: dict[str, Any] = {
        "setup": None,
        "source_config": [
            {
                "file_path": Path("./configs/source.yaml"),
                "options": {"encoding": "utf-8", "errors": "raise", "mode": "r"},
            }
        ],
        "storage": {
            "file_type": ResolveFileType.PARQUET,
        }
    }

    cleanup_file_or_folder(
        "./reports", minutes=10, name_format="%Y-%m-%d %H-%M-%S", dry_run=False
    )
    cleanup_file_or_folder("./logs", days=2, dry_run=False)
    cleanup_file_or_folder("./logs/error", days=2, dry_run=False)

    main(setup)

    # TODO: Global config for reader, writer, loader, storage,.., ex: excel reader: has_header=True, delimiter=, encoding=, ...