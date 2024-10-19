import argparse
from rich.console import Console
from rich.text import Text
from dooit.backport.migrate_from_v2 import Migrator2to3

console = Console()
print = console.print

VERSION = "3.0.0"


def run_dooit():
    from dooit.ui.tui import Dooit

    Dooit().run()


def migrate_data():
    migrator = Migrator2to3()
    migrator.migrate()


def handle_migration(args: argparse.Namespace):
    if args.migrate:
        print(Text("Migrating from v2 ...", style="green"))
        migrate_data()
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
    elif args.migrate:
        handle_migration(args)
    else:
        if Migrator2to3.check_for_old_data():
            print(
                Text.from_markup(
                    "Found todos for v2. Please migrate to v3 using [reverse] dooit --migrate [/reverse] first",
                    style="yellow",
                )
            )
            return

        run_dooit()


if __name__ == "__main__":
    main()
