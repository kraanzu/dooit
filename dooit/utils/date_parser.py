from datetime import datetime
from typing import Optional, Tuple
import parsedatetime
from os import environ

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")
cal = parsedatetime.Calendar()


def parse(value: str) -> Tuple[Optional[datetime], bool]:
    if value == "none":
        return None, True

    is_time_included = any(i in value.lower() for i in [":", "@", "at", "am", "pm"])

    parsed, ok = cal.parseDT(value)
    if not ok:
        return None, False

    if not is_time_included:
        parsed = datetime(parsed.year, parsed.month, parsed.day)

    return parsed, True
