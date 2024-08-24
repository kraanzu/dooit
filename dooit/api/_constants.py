from os import environ

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")
DATE_FORMAT = (
    "-".join(list(DATE_ORDER)).replace("D", "%d").replace("M", "%m").replace("Y", "%y")
)
TIME_FORMAT = "@%H:%M"
DURATION_LEGEND = {
    "m": "minute",
    "h": "hour",
    "d": "day",
    "w": "week",
}
CASUAL_FORMAT = "%d %h @ %H:%M"
