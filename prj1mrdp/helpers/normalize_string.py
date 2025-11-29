import re
from .logger import other_common_logger

@other_common_logger.catch
def normalize_string(column_name: str = "", type_casting: str = "snake_case"):
    """_summary_

    Args:
        column_name (str, optional): _description_. Defaults to "".
        type_casting (str, optional): _description_. Defaults to "snake_case".
    """

    if not column_name:
        raise ValueError("Column name is empty")

    if not isinstance(column_name, str):
        column_name = str(column_name)

    # Trim and lowercase
    column_name = column_name.strip()

    # Insert space before capitals (e.g., "SalesData" -> "Sales Data")
    column_name = re.sub(r'(?<=[a-z0-9])([A-Z])', r' \1', column_name)

    # Replace non-alphanumeric chars except underscore with space
    column_name = re.sub(r'[^a-zA-Z0-9_]+', ' ', column_name)

    # Collapse multiple underscores or spaces to a single underscore
    column_name = re.sub(r'[\s_]+', '_', column_name)

    # Lowercase final result and trim underscores
    column_name =  column_name.lower().strip('_')

    # if type_casting == "snake_case":
    #     column_name = "_".join(column_name)
    # # elif type_casting == "camelCase":
    # #     column_name = column_name[0] + "".join(w.title() for w in column_name[1:])
    # # elif type_casting == "PascalCase":
    # #     column_name = "".join(w.title() for w in column_name)
    # else:
    #     raise ValueError(f"Type casting {type_casting} is not supported")

    return column_name