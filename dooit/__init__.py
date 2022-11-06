import argparse
import pkg_resources
from .ui.tui import Dooit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    args = parser.parse_args()

    if args.version:
        ver = pkg_resources.get_distribution("dooit").version
        print(f"dooit - {ver}")
    else:
        Dooit.run()
