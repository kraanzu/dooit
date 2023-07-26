import dateutil.parser
from os import environ

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")


def parse(value: str):
    if value == "none":
        return None

    return dateutil.parser.parse(value)
