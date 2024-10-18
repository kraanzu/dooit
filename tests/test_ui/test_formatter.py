from rich.text import Text
from rich.style import Style
from dooit.api.workspace import Workspace
from dooit.ui.api.api_components.formatters import FormatterStore
from dooit.ui.api.dooit_api import DooitAPI
from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit


def set_italic(value: str, _: Workspace) -> str:
    text_value = Text(value)
    text_value.highlight_words(["test"], Style(italic=True))
    return text_value.markup


def add_icon(value: str, _: Workspace) -> str:
    if "test" in value:
        return f"[icon] {value}"
    else:
        return value


def setup(api: DooitAPI):
    store = FormatterStore(lambda: None, api)
    w = Workspace(description="this is a test description")
    return store, w


async def test_no_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w = setup(app.api)

        formatted = store.format_value(w.description, w)
        assert formatted == "this is a test description"


async def test_basic_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w = setup(app.api)

        store.add(set_italic)
        formatted = store.format_value(w.description, w)
        assert formatted == "this is a [italic]test[/italic] description"


async def test_multiple_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w = setup(app.api)

        store.add(set_italic)
        store.add(add_icon)
        formatted = store.format_value(w.description, w)
        assert formatted == "[icon] this is a test description"
