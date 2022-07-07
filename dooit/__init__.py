import pkg_resources
import argparse
import psutil
from .ui.tui import Doit


def is_running() -> bool:
    counter = 0
    try:
        for process in psutil.process_iter():
            counter += process.name() in ["dooit", "dooit.exe"]
    except psutil.NoSuchProcess:
        pass

    return counter > 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    args = parser.parse_args()

    if args.version:
        ver = pkg_resources.get_distribution("dooit").version
        print(f"dooit - {ver}")
    else:
        if is_running():
            exit(print("One instance of dooit is already running!\nQuiting..."))

        Doit.run()
