import re

from src.common.logger import logger


@logger.catch
def normalize_string(input_str: str = "", type_casting: str = "snake_case") -> str:
    """Normalize string.

    Args:
        input_str (str, optional): String to normalize. Defaults to "".
        type_casting (str, optional): Type casting string. Defaults to "snake_case".
    Return:
        str
    """

    if not input_str:
        raise ValueError("Column name is empty")

    if not isinstance(input_str, str):
        input_str = str(input_str)

    # Trim and lowercase
    input_str = input_str.strip()

    # Insert space before capitals (e.g., "SalesData" -> "Sales Data")
    input_str = re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", input_str)

    # Replace non-alphanumeric chars except underscore with space
    input_str = re.sub(r"[^a-zA-Z0-9_]+", " ", input_str)

    # Collapse multiple underscores or spaces to a single underscore
    input_str = re.sub(r"[\s_]+", "_", input_str)

    # Lowercase final result and trim underscores
    input_str = input_str.lower().strip("_")

    if type_casting == "snake_case":
        input_str = "_".join(input_str)
    elif type_casting == "camelCase":
        input_str = input_str[0] + "".join(w.title() for w in input_str[1:])
    elif type_casting == "PascalCase":
        input_str = "".join(w.title() for w in input_str)
    else:
        raise ValueError(f"Type casting {type_casting} is not supported")

    return input_str
