from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit


async def test_help_screen_mount():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await app.push_screen("help")
