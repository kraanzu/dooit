from datetime import datetime
from typing import Optional, Tuple
from dateutil import parser
from os import environ

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")


def parse(value: str) -> Tuple[Optional[datetime], bool]:
    try:
        return parser.parse(value), True
    except:
        return None, False
