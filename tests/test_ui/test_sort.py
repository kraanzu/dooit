from pytest import raises
from textual.widgets import ContentSwitcher
from dooit.api.exceptions import NoNodeError
from dooit.ui.widgets.trees.todos_tree import TodosTree
from dooit.ui.widgets.trees.workspaces_tree import WorkspacesTree
from dooit.ui.widgets.bars import SortBar

from tests.test_ui.ui_base import run_pilot, create_and_move_to_todo
from dooit.ui.tui import Dooit


async def test_search_on_workspace():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        api = app.api

        wtree = app.workspace_tree

        with raises(NoNodeError):
            api.start_sort()

        wtree.add_sibling()
        await pilot.press(*list("zzz"))
        await pilot.press("escape")

        api.start_sort()
        await pilot.pause()

        sort_bar = app.bar_switcher.visible_content
        assert isinstance(sort_bar, SortBar)

        assert len(sort_bar.options) == 2  # reverse and description


async def test_search_on_todo():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        api = app.api

        tree = await create_and_move_to_todo(pilot)

        with raises(NoNodeError):
            api.start_sort()

        tree.add_sibling()
        await pilot.press("escape")

        api.start_sort()
        await pilot.pause()

        sort_bar = app.bar_switcher.visible_content
        assert isinstance(sort_bar, SortBar)

        assert len(sort_bar.options) == 7  # reverse and description
