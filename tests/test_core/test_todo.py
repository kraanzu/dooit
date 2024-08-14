from sqlalchemy import select
from tests.test_core._base import CoreTestBase
from dooit.api import Todo, Workspace


class TestTodo(CoreTestBase):
    def test_todo_creation(self):
        for _ in range(5):
            t = Todo()
            t.save(session=self.session)

        query = select(Todo)
        result = self.session.execute(query).scalars().all()
        self.assertEqual(len(result), 5)

    def test_todo_siblings_by_creation(self):
        workspace = Workspace()
        workspace.save(session=self.session)

        for _ in range(5):
            todo = Todo(parent_workspace=workspace)
            todo.save(session=self.session)

        query = select(Todo)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None
        self.assertEqual(len(workspace.get_siblings(session=self.session)), 5)
