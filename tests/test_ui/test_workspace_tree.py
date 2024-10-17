from pytest import raises
from textual.widgets import ContentSwitcher
from dooit.api.exceptions import NoNodeError
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

        await pilot.pause()

        current = app.query_one(
            "#todo_switcher", expect_type=ContentSwitcher
        ).visible_content
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
        await pilot.press("escape")
        await pilot.pause()

        wtree.add_sibling()
        assert wtree.highlighted == 1


async def test_workspace_remove_cancelled():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        wtree = app.workspace_tree

        wtree.add_sibling()
        await pilot.press("escape")
        wtree.add_sibling()
        await pilot.press("escape")

        w1 = wtree.current_model

        current = app.query_one(
            "#todo_switcher", expect_type=ContentSwitcher
        ).visible_content
        assert current is not None
        assert current.id == TodosTree(w1).id

        wtree.remove_node()
        await pilot.pause()
        await pilot.press("n")
        await pilot.pause()

        w2 = wtree.current_model
        current = app.query_one(
            "#todo_switcher", expect_type=ContentSwitcher
        ).visible_content
        assert current is not None
        assert current.id == TodosTree(w2).id

        assert w1.id == w2.id


async def test_workspace_remove():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        wtree = app.workspace_tree

        wtree.add_sibling()
        await pilot.press("escape")
        wtree.add_sibling()
        await pilot.press("escape")

        w1 = wtree.current_model

        current = app.query_one(
            "#todo_switcher", expect_type=ContentSwitcher
        ).visible_content
        assert current is not None
        assert current.id == TodosTree(w1).id

        wtree.remove_node()
        await pilot.pause()
        await pilot.press("y")
        await pilot.pause()

        w2 = wtree.current_model
        current = app.query_one(
            "#todo_switcher", expect_type=ContentSwitcher
        ).visible_content
        assert current is not None
        assert current.id == TodosTree(w2).id

        assert w1.id != w2.id


async def test_no_node_error():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        wtree = app.workspace_tree

        with raises(NoNodeError):
            wtree.remove_node()