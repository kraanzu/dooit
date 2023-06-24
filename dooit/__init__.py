import argparse
from importlib.metadata import version
from .ui.tui import Dooit

from .Tests import Test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("-t", "--test", help="Make test", action="store_true", default=False)
    args = parser.parse_args()

    if args.version:
        ver = version("dooit")
        print(f"dooit - {ver}")
    elif args.test:
        Test.run()
    else:
        Dooit().run()
