import pandas as pd
# from .logger import logger_wrapper
from .logger import other_common_logger

@other_common_logger.catch
def read_csv_file(file_path = '', chunk_size: str = 1_000):
  """
  Read an csv file and return a DataFrame.

  Args:
    file_path (str): The path to the csv file.

  Returns:
    pd.DataFrame: A DataFrame containing the data from the csv file.
  """
  other_common_logger.info(f"Start reading csv file: {file_path} start")
  df = []
  with pd.read_csv(file_path, iterator=True, chunksize=chunk_size) as reader:
      for chunk in reader:
          df = pd.concat([df, chunk])
  other_common_logger.info(f"Complete reading csv file: {file_path}")
  return df