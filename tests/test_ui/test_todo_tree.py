from pytest import raises
from dooit.api.exceptions import NoNodeError
from dooit.ui.api.widgets import TodoWidget
from dooit.ui.widgets.renderers.base_renderer import BaseRenderer
from dooit.ui.widgets.trees.todos_tree import TodosTree
from tests.test_ui.ui_base import run_pilot, create_and_move_to_todo
from dooit.ui.tui import Dooit


def custom_formatter(value, todo):
    return "??"


async def test_todo_tree_focus():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await create_and_move_to_todo(pilot)

        ttree = app.focused
        assert isinstance(ttree, TodosTree)


async def test_todo_formatter():
    def get_formatted(renderer: BaseRenderer, attr: str):
        component = renderer._get_component(attr)
        formatter = renderer.tree.formatter
        return getattr(formatter, attr).format_value(
            component.model_value, component.model
        )

    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await create_and_move_to_todo(pilot)

        ttree = app.focused
        assert isinstance(ttree, TodosTree)

        ttree.add_sibling()
        await pilot.press(*list("nixos"))
        await pilot.press("escape")

        renderer = ttree.current
        assert get_formatted(renderer, "description") == "nixos"

        app.api.formatter.todos.description.add(custom_formatter)
        assert get_formatted(renderer, "description") == "??"


async def test_no_node_error():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await create_and_move_to_todo(pilot)

        ttree = app.focused
        assert isinstance(ttree, TodosTree)

        with raises(NoNodeError):
            ttree.current


async def test_todo_tree_layout():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await create_and_move_to_todo(pilot)

        ttree = app.focused
        assert isinstance(ttree, TodosTree)

        ttree.add_sibling()
        await pilot.press(*list("nixos"))
        await pilot.press("escape")

        table = ttree.current.make_renderable()
        assert table.columns[0].header == "status"

        app.api.layouts.todo_layout = [TodoWidget.description]
        table = ttree.current.make_renderable()
        assert table.columns[0].header == "description"
