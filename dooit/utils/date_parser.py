from datetime import datetime
from typing import Optional
import parsedatetime
from os import environ

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")
cal = parsedatetime.Calendar()


def parse(value: str) -> Optional[datetime]:
    if value == "none":
        return None

    return cal.parseDT(value)[0]
