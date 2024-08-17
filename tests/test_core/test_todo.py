from sqlalchemy import select
from tests.test_core._base import CoreTestBase
from dooit.api import Todo, Workspace


class TestTodo(CoreTestBase):
    def test_todo_creation(self):
        workspace = Workspace()

        for _ in range(5):
            todo = Todo(parent_workspace=workspace)
            todo.save()

        result = Todo.all()
        self.assertEqual(len(result), 5)

        indexs = sorted([t.order_index for t in result])

        self.assertEqual(indexs, [0, 1, 2, 3, 4])

    def test_sibling_methods(self):
        workspace = Workspace()

        for _ in range(5):
            todo = Todo(parent_workspace=workspace)
            todo.save()

        query = select(Todo)
        todo = self.session.execute(query).scalars().first()

        assert todo is not None

        siblings = todo.siblings
        index_ids = [w.order_index for w in siblings]
        self.assertEqual(index_ids, [0, 1, 2, 3, 4])
        self.assertTrue(siblings[0].is_first_sibling())
        self.assertTrue(siblings[-1].is_last_sibling())

    def test_todo_siblings_by_creation(self):
        workspace = Workspace()
        workspace.save()

        for _ in range(5):
            todo = Todo(parent_workspace=workspace)
            todo.save()

        query = select(Todo)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None
        self.assertEqual(len(workspace.siblings), 5)

    def test_parent_kind(self):
        workspace = Workspace()
        workspace.save()

        todo = Todo(parent_workspace=workspace)
        todo.save()

        self.assertFalse(todo.has_same_parent_kind)

        todo2 = Todo(parent_todo=todo)
        todo2.save()

        self.assertTrue(todo2.has_same_parent_kind)

    def test_without_parent(self):
        todo = Todo()

        with self.assertRaises(ValueError):
            todo.save()

    def test_with_both_parents(self):
        todo = Todo(parent_workspace=Workspace(), parent_todo=Todo())

        with self.assertRaises(ValueError):
            todo.save()

    def test_sibling_add(self):
        w = Workspace()
        w.save()

        t = w.add_todo()
        w.add_todo()

        t2 = t.add_sibling()

        self.assertEqual(len(t.siblings), 3)
        self.assertEqual(len(t2.siblings), 3)
        self.assertEqual(t2.order_index, 1)
