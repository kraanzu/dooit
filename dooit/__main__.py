import argparse
from rich.console import Console
from rich.text import Text

console = Console()
print = console.print

VERSION = "3.0.0"


def run_dooit():
    from dooit.ui.tui import Dooit

    Dooit().run()


def v2_exists() -> bool:
    return True


def handle_migration(args: argparse.Namespace):
    if args.migrate:
        print(Text("Migrating from v2 ...", style="green"))
        # migrate()
    else:
        print(
            Text.from_markup(
                "Found todos for v2. Please migrate to v3 using [reverse] dooit --migrate [/reverse] first",
                style="yellow",
            )
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("--migrate", help="Migrate from v2", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(f"dooit - {VERSION}")
    else:
        if v2_exists():
            handle_migration(args)
            return

        run_dooit()


if __name__ == "__main__":
    main()
