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
    if "123" in value:
        return f"[icon] {value}"
    else:
        return value


def setup(api: DooitAPI):
    store = FormatterStore(lambda: None, api)
    w1 = Workspace(description="this is a test description")
    w2 = Workspace(description="another description 123")
    return store, w1, w2


async def test_no_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, w2 = setup(app.api)

        formatted = store.format_value(w1.description, w1)
        assert formatted == "this is a test description"

        formatted = store.format_value(w2.description, w2)
        assert formatted == "another description 123"


async def test_basic_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, w2 = setup(app.api)

        store.add(set_italic)
        formatted = store.format_value(w1.description, w1)
        assert formatted == "this is a [italic]test[/italic] description"

        formatted = store.format_value(w2.description, w2)
        assert formatted == "another description 123"


async def test_multiple_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, w2 = setup(app.api)

        store.add(set_italic)
        store.add(add_icon)
        formatted = store.format_value(w1.description, w1)
        assert formatted == "this is a test description"

        formatted = store.format_value(w2.description, w2)
        assert formatted == "[icon] another description 123"
