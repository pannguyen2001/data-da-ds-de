import pandas as pd
# from .logger import logger_wrapper
from .logger import other_common_logger

@other_common_logger.catch
def read_excel_file(file_path ='', sheet_name='Sheet1'):
  """
  Read an Excel file and return a DataFrame.

  Args:
    file_path (str): The path to the Excel file.
    sheet_name (str): The name of the sheet to read.

  Returns:
    pd.DataFrame: A DataFrame containing the data from the Excel file.
  """
  other_common_logger.info(f"Start reading excel file: {file_path}")
  df = pd.read_excel(file_path, sheet_name)
  other_common_logger.info(f"Complete reading excel file: {file_path}")
  return df