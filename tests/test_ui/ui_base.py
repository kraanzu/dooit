from textual.pilot import Pilot
from dooit.ui.tui import Dooit

TEMP_CONN = "sqlite:///:memory:"


def run_pilot():
    return Dooit(connection_string=TEMP_CONN).run_test()


async def create_and_move_to_todo(pilot: Pilot):
    app = pilot.app
    assert isinstance(app, Dooit)

    wtree = app.workspace_tree
    wtree.add_sibling()
    await pilot.pause()

    await pilot.press("escape")
    await pilot.pause()

    app.api.switch_focus()
    await pilot.pause()
