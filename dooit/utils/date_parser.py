from dateparser import parse as dateparse
from threading import Thread
from os import environ

# from dooit.utils.conf_reader import Config

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")


def parse(value: str):
    if value == "none":
        return None

    return dateparse(value, settings={"DATE_ORDER": DATE_ORDER})


# HACK: Deal with dateparser slowness
Thread(target=parse, args=("",), daemon=True).start()
