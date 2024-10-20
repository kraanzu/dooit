import click
from pathlib import Path
from platformdirs import user_data_dir

OLD_CONFIG = Path(user_data_dir("dooit")) / "todo.yaml"
VERSION = "3.0.0"


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    help="Show version and exit.",
)
@click.pass_context
def main(ctx, version: bool) -> None:
    """Main entry point for the command-line interface."""
    if version:
        return print(f"dooit - {VERSION}")

    if ctx.invoked_subcommand is None:
        # Check for old configuration and show warning if needed
        if OLD_CONFIG.exists():
            from dooit.utils.cli_logger import logger

            logger.warn(
                "Found todos for v2.",
                "Please migrate to v3 using [reverse] dooit migrate [/reverse] first.",
            )
            return

        # Run the main Dooit application if no subcommand is invoked
        from dooit.ui.tui import Dooit

        Dooit().run()


@main.command(help="Migrate data from v2 to v3.")
def migrate() -> None:
    """Perform migration from v2."""
    from dooit.utils.cli_logger import logger

    logger.info("Migrating from v2 ...")
    from dooit.backport.migrate_from_v2 import Migrator2to3

    migrator = Migrator2to3()
    migrator.migrate()


if __name__ == "__main__":
    main()
