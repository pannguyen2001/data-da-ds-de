import pandas as pd
import os
from loguru import logger
from helpers.logger_wrapper import logger_wrapper
from string import Template

success_message: str = Template("""Write data successfully:
    Sheet name: ${sheet_name}
    File path: ${file_path}""")


@logger_wrapper
def write_excel_file(
    data_input=None,
    file_path='file_path.xlsx',
    sheet_name='Sheet1',
    index=False,
    start_row=0,
    start_col=0,
    *args,
    **kwargs
) -> None:
    is_file_exist: bool = os.path.isfile(file_path)
    if not is_file_exist:
        logger.info(f"Write data to new file: {file_path}")

        df = pd.DataFrame(data=data_input)
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=index,
                startrow=start_row,
                startcol=start_col,
                *args,
                **kwargs
            )
            logger.success(
                success_message.safe_substitute(
                    sheet_name=sheet_name,
                    file_path=file_path
                )
            )
        return

    df = pd.ExcelFile(file_path)
    if sheet_name in df.sheet_names:
        logger.info(f"Write data to existing sheet: {sheet_name}")

        with pd.ExcelWriter(
            file_path,
            engine='openpyxl',
            mode='a',
            if_sheet_exists="overlay"
        ) as writer:
            df = pd.DataFrame(data=data_input)
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=index,
                startrow=start_row,
                startcol=start_col,
                *args,
                **kwargs
            )
            logger.success(
                success_message.safe_substitute(
                    sheet_name=sheet_name,
                    file_path=file_path
                )
            )
            return

    logger.info(f"Write data to new sheet: {sheet_name}")

    with pd.ExcelWriter(
        file_path,
        engine='openpyxl',
        mode='a'
    ) as writer:
        df = pd.DataFrame(data=data_input)
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=index,
            startrow=start_row,
            startcol=start_col,
            *args,
            **kwargs
        )
        logger.success(
            success_message.safe_substitute(
                sheet_name=sheet_name,
                file_path=file_path
            )
        )
        return
