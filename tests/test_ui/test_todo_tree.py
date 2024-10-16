from dooit.ui.widgets.trees.todos_tree import TodosTree
from tests.test_ui.ui_base import run_pilot, create_and_move_to_todo
from dooit.ui.tui import Dooit


async def test_todo_tree_focus():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)

        await create_and_move_to_todo(pilot)

        ttree = app.focused
        assert isinstance(ttree, TodosTree)
