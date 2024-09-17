from textual.pilot import Pilot
from dooit.ui.tui import Dooit
from dooit.ui.widgets.trees import WorkspacesTree
TEMP_CONN = "sqlite:///:memory:"


async def test_startup():
    async with Dooit(connection_string=TEMP_CONN).run_test() as pilot:
        assert pilot.app.is_running
