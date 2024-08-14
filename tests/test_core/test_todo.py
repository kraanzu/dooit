from sqlalchemy import select
from tests.test_core._base import CoreTestBase
from dooit.api import Todo, Workspace


class TestTodo(CoreTestBase):
    def test_todo_creation(self):
        workspace = Workspace()

        for _ in range(5):
            t = Todo(parent_workspace=workspace)
            t.save(session=self.session)

        query = select(Todo)
        result = self.session.execute(query).scalars().all()
        self.assertEqual(len(result), 5)

        index_ids = sorted([t.order_index for t in result])
        self.assertEqual(index_ids, [1, 2, 3, 4, 5])

    def test_sibling_methods(self):
        workspace = Workspace()

        for _ in range(5):
            todo = Todo(parent_workspace=workspace)
            todo.save(self.session)

        query = select(Todo)
        todo = self.session.execute(query).scalars().first()

        assert todo is not None

        siblings = todo.get_siblings(session=self.session)
        index_ids = [w.order_index for w in siblings]
        self.assertEqual(index_ids, [1, 2, 3, 4, 5])
        self.assertTrue(siblings[0].is_first_sibling(session=self.session))
        self.assertTrue(siblings[-1].is_last_sibling(session=self.session))

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

    def test_parent_kind(self):
        workspace = Workspace()
        workspace.save(self.session)

        todo = Todo(parent_workspace=workspace)
        todo.save(self.session)

        self.assertFalse(todo.has_same_parent_kind)

        todo2 = Todo(parent_todo=todo)
        todo2.save(self.session)

        self.assertTrue(todo2.has_same_parent_kind)
