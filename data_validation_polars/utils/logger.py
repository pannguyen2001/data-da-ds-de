import sys
from loguru import logger
from string import Template
from configs.constants import date_today

error_template = Template("""[${funct_name}] has error:
${error}""")

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<level>[{level}]</level>[<green>{time:YYYY-MM-DD HH:mm:ss}</green>][<cyan>{name}:{function}:{line}</cyan>] <level>{message}</level>",
)

logger.add(
    f"./logs/{date_today}.log",
    colorize=False,
    format="[{level}][{time:YYYY-MM-DD HH:mm:ss}][{name}:{function}:{line}] {message}"
)
