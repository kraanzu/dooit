from datetime import datetime
from typing import Optional
import parsedatetime
from os import environ

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")
cal = parsedatetime.Calendar()


def parse(value: str) -> Optional[datetime]:
    if value == "none":
        return None

    is_time_included = any(i in value.lower() for i in [":", "@", "at", "am", "pm"])

    parsed: datetime = cal.parseDT(value)[0]
    if not is_time_included:
        parsed = datetime(parsed.year, parsed.month, parsed.day)

    return parsed
