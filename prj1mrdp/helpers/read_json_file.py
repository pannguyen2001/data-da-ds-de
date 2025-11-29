import pandas as pd
# from .logger import logger_wrapper
from .logger import other_common_logger

@other_common_logger.catch
def read_json_file(file_path = ''):
  """
  """
  other_common_logger.info(f"Start reading json file: {file_path}")
  df = pd.read_json(file_path)
  if df.empty:
    raise ValueError("File is empty.")
  other_common_logger.info(f"Complete reading json file: {file_path}")
  return df