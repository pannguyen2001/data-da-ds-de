import pandas as pd
from helpers.logger_wrapper import logger_wrapper
from string import Template

success_message: str = Template("""Read data successfully:
    Sheet name: ${sheet_name}
    File path: ${file_path}""")


@logger_wrapper
def read_excel_file(
    file_path: str = "",
    sheet_name: str = "",
    *args,
    **kwargs
) -> pd.DataFrame:
    if not file_path:
        logger.error("File path is required")
        return None
    if not sheet_name:
        logger.error("Sheet name is required")
        return None

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        *args,
        **kwargs
    )

    logger.success(
        success_message.safe_substitute(
            sheet_name=sheet_name,
            file_path=file_path
        )
    )
    return df
