from asyncio import sleep
from textual.widgets import ContentSwitcher
from dooit.ui.widgets.trees.todos_tree import TodosTree
from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit


async def test_workspaces_tree():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        wtree = app.workspace_tree

        assert len(wtree._options) == 0

        # basic addition
        wtree.add_workspace()
        wtree.add_workspace()
        wtree.add_workspace()
        w = wtree.add_workspace()

        assert len(wtree._options) == 4

        # highlights
        wtree.highlight_id(w)
        assert wtree.highlighted == 3  # n-1

        await sleep(0.5)

        current = app.query_one("#todo_switcher", expect_type=ContentSwitcher).visible_content
        assert current is not None
        assert current.id == TodosTree(wtree.current_model).id

        # child nodes
        w = wtree.add_child_node()
        assert len(wtree._options) == 5
        assert wtree.highlighted == 4

        # nested nodes
        wtree.toggle_expand()
        assert len(wtree._options) == 5

        wtree.toggle_expand_parent()
        assert len(wtree._options) == 4

        wtree.toggle_expand()
        assert len(wtree._options) == 5

        # switch


async def test_base_addition():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        wtree = app.workspace_tree

        wtree.add_sibling()
        assert wtree.highlighted == 0
        await sleep(0.5)

        wtree.add_sibling()
        assert wtree.highlighted == 1
