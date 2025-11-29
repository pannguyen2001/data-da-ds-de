import pandas as pd
import os.path
from string import Template
# from .logger import logger_wrapper
from .logger import other_common_logger

write_successfully_template = Template("""Write data to excel file successfully.
Detail info:
    Sheet name: ${sheet_name}.
    File: ${file_out}.""")

@other_common_logger.catch
def write_data_to_excel_file(
    data_input: pd.DataFrame,
    file_out: str = 'file_out.xlsx',
    sheet_name: str ='Sheet1',
    is_index_input: bool = False,
    start_row: int = 0,
    start_col: int = 0,
    mode: str = 'a'
    ):
    """
    Write data to excel file

    Args:
        data_input (pd.DataFrame, optional): Data need write. Defaults to pd.DataFrame().
        file_out (str, optional): File path to write. Defaults to 'file_out.xlsx'.
        sheet_name (str, optional): Sheet name. Defaults to 'Sheet1'.
        is_index_input (bool, optional): Determine data having index or not. Defaults to False.
        start_row (int, optional): Row to start write. Defaults to 0.
        start_col (int, optional): Column to start write. Defaults to 0.
        mode (str, optional): Mode write to file. Can be 'a' or 'w'. Defaults to 'a'.
    """
    is_file_exist= os.path.isfile(file_out)

    if not is_file_exist:
        other_common_logger.info("Write data to new file.")
        df= pd.DataFrame(data= data_input)
        df.to_excel(file_out, sheet_name=sheet_name , index=is_index_input)
    else:
        df = pd.ExcelFile(file_out)
        if sheet_name in df.sheet_names:
            other_common_logger.info(f"Write data to existing sheet {sheet_name}.")

            if mode == 'w':
                other_common_logger.info("Write data with mode: replace (clear all before write).")
                with pd.ExcelWriter(file_out, engine='openpyxl', mode='a', if_sheet_exists="replace") as writer:
                    df= pd.DataFrame(data= data_input)
                    df.to_excel(writer, sheet_name=sheet_name, index=is_index_input)
            else:
                other_common_logger.info("Write data with mode: overlay.")
                with pd.ExcelWriter(file_out, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
                    df= pd.DataFrame(data= data_input)
                    df.to_excel(writer, sheet_name=sheet_name, index=is_index_input, startrow= start_row, startcol= start_col )
        else:
            other_common_logger.info(f"Write data to new sheet {sheet_name}.")
            with pd.ExcelWriter(file_out, engine='openpyxl', mode='a') as writer:
                df= pd.DataFrame(data= data_input)
                df.to_excel(writer, sheet_name=sheet_name, index=is_index_input, startrow= start_row, startcol= start_col)

    other_common_logger.info(write_successfully_template.safe_substitute(sheet_name=sheet_name, file_out=file_out))
    return True