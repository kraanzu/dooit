from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit
from dooit.ui.screens import HelpScreen


async def test_help_screen_mount():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        # test if help screen is mounted
        await app.push_screen("help")
        assert app.screen.__class__ == HelpScreen

        await app.push_screen("main")

        # test with keybinding
        await pilot.press("?")
        assert app.screen.__class__ == HelpScreen
