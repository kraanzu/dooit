import argparse
from dooit.ui.tui import Dooit

VERSION = "3.0.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(f"dooit - {VERSION}")
    else:
        from dooit.ui.tui import Dooit
        Dooit().run()


if __name__ == "__main__":
    main()
