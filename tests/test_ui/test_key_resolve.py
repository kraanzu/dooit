from textual import events
from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit
from dooit.ui.screens import MainScreen


async def test_base_screen_keys():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await pilot.pause()
        screen = app.screen

        assert isinstance(screen, MainScreen)

        assert screen.resolve_key(events.Key("home", None)) == "home"
        assert screen.resolve_key(events.Key("space", " ")) == " "
