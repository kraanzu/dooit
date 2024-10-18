from tests.test_core.core_base import CoreTestBase
from dooit.api.workspace import Workspace
from dooit.ui.api.api_components.formatters import FormatterStore
from rich.text import Text
from rich.style import Style


def set_italic(value: str, _: Workspace) -> str:
    text_value = Text(value)
    text_value.highlight_words(["test"], Style(italic=True))
    return text_value.markup


def add_icon(value: str, _: Workspace) -> str:
    if "test" in value:
        return f"[icon] {value}"
    else:
        return value


class FormatterTest(CoreTestBase):
    def setUp(self):
        super().setUp()
        self.store = FormatterStore(lambda: None)
        self.w = Workspace(description="this is a test description")

    def test_no_formatting(self):
        formatted = self.store.format_value(self.w.description, self.w)
        assert formatted == "this is a test description"

    def test_basic_formatting(self):
        self.store.add(set_italic)
        formatted = self.store.format_value(self.w.description, self.w)
        assert formatted == "this is a [italic]test[/italic] description"

    def test_multiple_formatting(self):
        self.store.add(set_italic)
        self.store.add(add_icon)
        formatted = self.store.format_value(self.w.description, self.w)
        assert formatted == "[icon] this is a test description"
