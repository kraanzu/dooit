import argparse
from dooit.utils.cli_logger import logger
from dooit.backport.migrate_from_v2 import Migrator2to3


VERSION = "3.0.0"


def run_dooit():
    from dooit.ui.tui import Dooit

    Dooit().run()


def migrate_data():
    migrator = Migrator2to3()
    migrator.migrate()


def handle_migration():
    logger.info("Migrating from v2 ...")
    migrate_data()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("--migrate", help="Migrate from v2", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(f"dooit - {VERSION}")
    elif args.migrate:
        handle_migration()
    else:
        if Migrator2to3.check_for_old_data():
            logger.warn(
                "Found todos for v2.",
                "Please migrate to v3 using [reverse] dooit --migrate [/reverse] first",
            )
            return

        run_dooit()


if __name__ == "__main__":
    main()
