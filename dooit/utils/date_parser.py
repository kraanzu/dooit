from datetime import datetime
from typing import Optional, Tuple
from dateutil import parser


def parse(value: str) -> Tuple[Optional[datetime], bool]:
    try:
        return parser.parse(value), True
    except parser.ParserError:
        return None, False
