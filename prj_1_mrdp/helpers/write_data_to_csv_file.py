import pandas as pd
from typing import Any, Dict
# from .logger import logger_wrapper
from .logger import other_common_logger

@other_common_logger.catch
def write_data_to_csv_file(data_input: pd.DataFrame|Dict, header_input: Any = None, file_out: str = 'result.csv'):
    """
    Write data to csv file

    Args:
        data_input (pd.DataFrame | Dict): Data need write to csv file.
        header_input (Any, optional): Header of csv file. Defaults to None.
        file_out (str, optional): File path to write. Defaults to 'fileCSVOut.csv'.
    """
    df = pd.DataFrame(data= data_input, columns=header_input)
    df.to_csv(file_out)
    other_common_logger.info(f"Complete write data to file: {file_out}.")
    return True
