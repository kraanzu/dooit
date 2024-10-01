import argparse
from importlib.metadata import version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    args = parser.parse_args()

    if args.version:
        ver = version("dooit")
        print(f"dooit - {ver}")
    else:
        from dooit.ui.tui import Dooit
        Dooit().run()


if __name__ == "__main__":
    main()
