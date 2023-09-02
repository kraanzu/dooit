from datetime import datetime
from typing import Optional, Tuple
from dateutil import parser
from dooit.utils.conf_reader import config_man

DAY_FIRST = config_man.get("USE_DAY_FIRST")


def parse(value: str) -> Tuple[Optional[datetime], bool]:
    try:
        return parser.parse(value, dayfirst=DAY_FIRST), True
    except:
        return None, False
