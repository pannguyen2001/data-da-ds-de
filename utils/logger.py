import sys
from loguru import logger
from pathlib import Path
from constants import date_today, DataPipelineActivities, PROJECT_NAME, LoggerLevels

# ========== Format message ==========
"""
[MESSAGE_LEVEL] [datetime] [file_execute - line] - [DATA_PIPELINE_PHASE] [Sub phase] message
Description:
MESSAGE_LEVEL: DEBUG, INFO, WARNING,ERROR, CRITICAL: upper case, bold
DATA_PIPELINE_PHASE: COLLECTION, INGESTION, COMPUTING, STORAGE, CONSUMPTION, MANAGEMENT, GOVERNANCE
SERCURITY
OTHER
COMMON
Sub phase: ex: in collection: validate source, ingestion: quality, computing: cleaning,...
Datetime: YYYY-MM-DD HH:MM:SS
Message: clear content: error, info, variable: a = 1, ... beautiful format, if dict, use json.dumps() python
Can sort, filter, pagination by datetime, level, data pipeline phase, sub phase
"""

log_file = Path(f"./logs/{date_today}.log")
if not log_file.parent.exists():
    Path.mkdir("./logs", exist_ok=True, parents=True)
    log_file.touch()

# Debug
error_log_file = Path(f"./logs/error/{date_today}.log")
if not error_log_file.parent.exists():
    error_log_file.parent.mkdir("./logs/error",exist_ok=True, parents=True)
    error_log_file.touch()

# === Configure Loguru ===
# create log
logger.remove()
logger.level(name=LoggerLevels.DEBUG, color='<blue><bold>', icon='🔍')
logger.level(name=LoggerLevels.INFO, color='<green><bold>', icon='💡')
logger.level(name=LoggerLevels.SUCCESS, color='<cyan><bold>', icon='😀')
logger.level(name=LoggerLevels.WARNING, color='<yellow><bold>', icon='❕')
logger.level(name=LoggerLevels.ERROR, color='<red><bold>', icon='❌')
logger.level(name=LoggerLevels.CRITICAL, color='<white><bold>', icon='🚫')

logger.add(
    sys.stdout,
    colorize=True,
    level="DEBUG",
    format="<level>{level.icon}</level><level> {level}</level> [<level>{extra[project]}</level>][<level>{extra[phase]}:{extra[sub_phase]}</level>][<green>{time:YYYY-MM-DD HH:mm:ss}</green>][<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>]\n{message}\n",
    backtrace=True,
    diagnose=True,
    enqueue=True, # mutiple thread/processing
    )

logger.add(
    log_file,
    rotation="1 week",
    retention="1 month",
    level="DEBUG",
    format="[💡{level}][{extra[project]}][{extra[phase]}:{extra[sub_phase]}][{time:YYYY-MM-DD HH:mm:ss}][{name}:{function}:{line}]\n{message}\n",
    backtrace=True,
    diagnose=True,
    mode="a",
    enqueue=True,
    # serialize=True, # turn to json format, easy to send to slack, discord, etc.
)
# just for filter easier, can remove when complete debugging
logger.add(
    error_log_file,
    rotation="1 week",
    retention="1 month",
    level="WARNING",
    format="[{level}][{extra[project]}][{extra[phase]}:{extra[sub_phase]}][{time:YYYY-MM-DD HH:mm:ss}][{name}:{function}:{line}]\n{message}",
    backtrace=True,
    diagnose=True,
    mode="w",
    enqueue=True,
    # serialize=True,
)

logger = logger.bind(project=PROJECT_NAME)
common_phase_logger = logger.bind(phase=DataPipelineActivities.COMMON)
collection_phase_logger = logger.bind(phase=DataPipelineActivities.COLLECTION)
ingestion_phase_logger = logger.bind(phase=DataPipelineActivities.INGESTION)
computing_phase_logger = logger.bind(phase=DataPipelineActivities.COMPUTING)
storage_phase_logger = logger.bind(phase=DataPipelineActivities.STORAGE)
consumption_phase_logger = logger.bind(phase=DataPipelineActivities.CONSUMPTION)
management_phase_logger = logger.bind(phase=DataPipelineActivities.MANAGEMENT)
governance_phase_logger = logger.bind(phase=DataPipelineActivities.GOVERNANCE)
monitoring_phase_logger = logger.bind(phase=DataPipelineActivities.MONITORING)


# Sub phase common
other_common_logger = common_phase_logger.bind(sub_phase="other")



