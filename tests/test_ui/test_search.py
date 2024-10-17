from dooit.ui.widgets.trees.todos_tree import TodosTree
from tests.test_ui.ui_base import run_pilot, create_and_move_to_todo
from dooit.ui.tui import Dooit


async def test_search():
    async with run_pilot() as pilot:

        app = pilot.app
        assert isinstance(app, Dooit)

        async def create_todo(tree: TodosTree, description: str):
            tree.add_sibling()
            await pilot.press(*list(description))
            await pilot.press("escape")

        await create_and_move_to_todo(pilot)

        tree = app.focused
        assert isinstance(tree, TodosTree)

        items = ["apple", "apps", "applet", "apricot"]
        for item in items:
            await create_todo(tree, item)

        assert len(tree._options) == 4

        tree.start_search()
        await pilot.pause()

        await pilot.press("a")
        assert sum(i.disabled for i in tree._options) == 0

        await pilot.press("p", "p")
        assert sum(i.disabled for i in tree._options) == 1

        await pilot.press("l")
        assert sum(i.disabled for i in tree._options) == 2

        await pilot.press(*(["backspace"] * 4))
        assert sum(i.disabled for i in tree._options) == 0

        await pilot.press(*list("applet"))
        assert sum(i.disabled for i in tree._options) == 3

        # await pilot.press("enter")

        # await pilot.press("escape")
        # await pilot.pause()
        # assert sum(i.disabled for i in tree._options) == 0
