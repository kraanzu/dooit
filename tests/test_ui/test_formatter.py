from typing import Optional
from rich.text import Text
from rich.style import Style
from dooit.api.workspace import Workspace
from dooit.ui.api.api_components.formatters import FormatterStore
from dooit.ui.api.dooit_api import DooitAPI
from dooit.ui.api import extra_formatter
from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit


def set_italic(value: str, _: Workspace, api: DooitAPI) -> Optional[str]:
    text_value = Text(value)
    text_value.highlight_words(
        ["test"],
        Style(
            italic=True,
            color=api.vars.theme.red,
        ),
    )
    return text_value.markup


@extra_formatter
def add_icon(value: str, _: Workspace) -> Optional[str]:
    if "123" in value:
        return f"(icon) {value}"


def add_icon_skip_multiple(value: str, _: Workspace) -> Optional[str]:
    if "123" in value:
        return f"(icon) {value}"


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
        assert formatted.markup == "this is a test description"

        formatted = store.format_value(w2.description, w2)
        assert formatted.markup == "another description 123"


async def test_basic_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, w2 = setup(app.api)

        store.add(set_italic)
        formatted = store.format_value(w1.description, w1)
        assert (
            formatted.markup == "this is a [italic #bf616a]test[/italic #bf616a] description"
        )

        formatted = store.format_value(w2.description, w2)
        assert formatted.markup == "another description 123"


async def test_multiple_formatting():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, w2 = setup(app.api)

        store.add(set_italic)
        store.add(add_icon)
        formatted = store.format_value(w1.description, w1)
        assert (
            formatted.markup == "this is a [italic #bf616a]test[/italic #bf616a] description"
        )

        formatted = store.format_value(w2.description, w2)
        assert formatted.markup == "(icon) another description 123"


async def test_multiple_formatting_skip():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, w2 = setup(app.api)
        w2.description = "another description 123 test"

        store.add(set_italic)
        store.add(add_icon_skip_multiple)
        formatted = store.format_value(w1.description, w1)
        assert (
            formatted.markup == "this is a [italic #bf616a]test[/italic #bf616a] description"
        )

        formatted = store.format_value(w2.description, w2)
        assert formatted.markup == "(icon) another description 123 test"


async def test_multiple_formatting_toggle():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        store, w1, _ = setup(app.api)

        w1.description += " 123"

        store.add(set_italic, id="italic")
        store.add(add_icon, id="icon")
        formatted = store.format_value(w1.description, w1)
        assert (
            formatted.markup
            == "(icon) this is a [italic #bf616a]test[/italic #bf616a] description 123"
        )

        assert store.disable("italic")
        formatted = store.format_value(w1.description, w1)
        assert formatted.markup == "(icon) this is a test description 123"

        assert store.disable("icon")
        formatted = store.format_value(w1.description, w1)
        assert formatted.markup == "this is a test description 123"

        assert store.enable("italic")
        formatted = store.format_value(w1.description, w1)
        assert (
            formatted.markup
            == "this is a [italic #bf616a]test[/italic #bf616a] description 123"
        )

        assert not store.enable("random_gibberish_id")
        assert not store.disable("random_gibberish_id")

        store.remove("italic")
        formatted = store.format_value(w1.description, w1)
        assert formatted.markup == "this is a test description 123"
