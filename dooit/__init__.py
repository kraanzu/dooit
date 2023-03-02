import argparse
from importlib.metadata import version
from .ui.tui import Dooit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    args = parser.parse_args()

    if args.version:
        ver = version("dooit")
        print(f"dooit - {ver}")
    else:
        Dooit().run()
