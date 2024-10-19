import argparse
from pathlib import Path
from platformdirs import user_data_dir


OLD_CONFIG = Path(user_data_dir("dooit")) / "todo.yaml"
VERSION = "3.0.0"


def run_dooit():
    from dooit.ui.tui import Dooit

    Dooit().run()


def migrate_data():
    from dooit.backport.migrate_from_v2 import Migrator2to3

    migrator = Migrator2to3()
    migrator.migrate()


def handle_migration():
    from dooit.utils.cli_logger import logger

    logger.info("Migrating from v2 ...")
    migrate_data()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("--migrate", help="Migrate from v2", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(f"dooit - {VERSION}")
        return

    from dooit.utils.cli_logger import logger

    if args.migrate:
        handle_migration()
    else:
        if OLD_CONFIG.exists():
            logger.warn(
                "Found todos for v2.",
                "Please migrate to v3 using [reverse] dooit --migrate [/reverse] first",
            )
            return

        run_dooit()


if __name__ == "__main__":
    main()
