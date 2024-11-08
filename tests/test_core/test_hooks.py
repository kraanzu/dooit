from tests.test_core.core_base import CoreTestBase
from dooit.api import Workspace


class TestTodo(CoreTestBase):
    def setUp(self):
        super().setUp()
        self.default_workspace = Workspace()

    def test_todo_status_update_children(self):
        parent_todo = self.default_workspace.add_todo()
        child_todos = [parent_todo.add_todo() for _ in range(5)]

        self.assertTrue(parent_todo.is_pending)

        for child_todo in child_todos:
            child_todo.toggle_complete()

        self.assertFalse(parent_todo.is_pending)
