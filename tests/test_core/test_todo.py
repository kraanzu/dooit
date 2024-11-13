from typing import List, Tuple
from datetime import datetime, timedelta
from sqlalchemy import select
from pytest import raises
from dooit.api.exceptions import NoParentError, MultipleParentError
from tests.test_core.core_base import CoreTestBase
from dooit.api import Todo, Workspace


class TestTodo(CoreTestBase):
    def setUp(self):
        super().setUp()
        self.default_workspace = Workspace()

    def test_todo_creation(self):
        for _ in range(5):
            todo = Todo(parent_workspace=self.default_workspace)
            todo.save()

        result = Todo.all()
        self.assertEqual(len(result), 5)

        indexs = sorted([t.order_index for t in result])

        self.assertEqual(indexs, [0, 1, 2, 3, 4])

    def test_sibling_methods(self):
        for _ in range(5):
            todo = Todo(parent_workspace=self.default_workspace)
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
        for _ in range(5):
            todo = Todo(parent_workspace=self.default_workspace)
            todo.save()

        query = select(Todo)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None
        self.assertEqual(len(workspace.siblings), 5)

    def test_parent_kind(self):
        todo = Todo(parent_workspace=self.default_workspace)
        todo.save()

        self.assertFalse(todo.has_same_parent_kind)

        todo2 = Todo(parent_todo=todo)
        todo2.save()

        self.assertTrue(todo2.has_same_parent_kind)

    def test_without_parent(self):
        todo = Todo()

        with self.assertRaises(NoParentError):
            todo.save()

    def test_with_both_parents(self):
        w = self.default_workspace
        t = w.add_todo()

        todo = Todo(parent_workspace=w, parent_todo=t)

        with self.assertRaises(MultipleParentError):
            todo.save()

    def test_sibling_add(self):
        t = self.default_workspace.add_todo()
        self.default_workspace.add_todo()

        t2 = t.add_sibling()

        self.assertEqual(len(t.siblings), 3)
        self.assertEqual(len(t2.siblings), 3)
        self.assertEqual(t2.order_index, 1)

    def test_comparable_fields(self):
        fields = Todo.comparable_fields()
        expected_fields = [
            "description",
            "due",
            "effort",
            "recurrence",
            "urgency",
            "pending",
        ]
        self.assertEqual(fields, expected_fields)

    def test_nest_level(self):
        t = self.default_workspace.add_todo()
        self.assertEqual(t.nest_level, 0)

        t = t.add_todo()
        self.assertEqual(t.nest_level, 1)

        t = t.add_todo()
        self.assertEqual(t.nest_level, 2)

    def test_from_id(self):
        t = self.default_workspace.add_todo()
        _id = t.id
        t_from_id = Todo.from_id(str(_id))

        self.assertEqual(t_from_id, t)

    def test_toggle_complete(self):
        t = self.default_workspace.add_todo()
        self.assertTrue(t.pending)
        self.assertTrue(t.is_pending)
        self.assertFalse(t.is_completed)

        t.toggle_complete()
        self.assertFalse(t.pending)
        self.assertFalse(t.is_pending)
        self.assertTrue(t.is_completed)

    def test_toggle_complete_parent(self):
        t = self.default_workspace.add_todo()
        t1 = t.add_todo()
        t2 = t.add_todo()

        t1.toggle_complete()
        self.assertFalse(t.is_completed)

        t2.toggle_complete()
        self.assertTrue(t.is_completed)

        t1.toggle_complete()
        self.assertFalse(t.is_completed)

    def test_due_date_util(self):
        t = self.default_workspace.add_todo()
        self.assertFalse(t.due)
        self.assertFalse(t.is_overdue)
        self.assertFalse(t.is_due_today())
        self.assertEqual(t.status, "pending")

        t.due = datetime.now()
        self.assertTrue(t.is_overdue)
        self.assertTrue(t.due)
        self.assertTrue(t.is_due_today())
        self.assertEqual(t.status, "overdue")

        t.due = datetime.now() - timedelta(days=1)
        self.assertFalse(t.is_due_today())
        self.assertTrue(t.is_overdue)
        self.assertEqual(t.status, "overdue")

        t.due = datetime.now() + timedelta(days=1)
        self.assertFalse(t.is_overdue)
        self.assertEqual(t.status, "pending")

        t.toggle_complete()
        self.assertEqual(t.status, "completed")

    def test_tags(self):
        t = self.default_workspace.add_todo()
        t.description = "This is a @tag"
        self.assertEqual(t.tags, ["@tag"])

        t.description = "This is a @tag and @another"
        self.assertEqual(t.tags, ["@tag", "@another"])

        t.description = "This is a tag"
        self.assertEqual(t.tags, [])

    def test_urgency(self):
        t = self.default_workspace.add_todo()
        assert t.urgency == 1

        t.decrease_urgency()
        assert t.urgency == 1

        t.increase_urgency()
        t.increase_urgency()
        t.increase_urgency()
        t.increase_urgency()
        t.increase_urgency()

        assert t.urgency == 4

    def test_recurrence_change(self):
        t = self.default_workspace.add_todo()
        t.due = datetime.strptime("2021-01-01", "%Y-%m-%d")
        t.recurrence = timedelta(days=1)
        t.save()

        assert t.due == datetime.strptime("2021-01-01", "%Y-%m-%d")
        t.toggle_complete()
        assert t.due == datetime.strptime("2021-01-02", "%Y-%m-%d")

    def test_sort_invalid(self):
        t = self.default_workspace.add_todo()

        with raises(AttributeError):
            t.sort_siblings("???????")

    def _sort_before_and_after(self, field) -> Tuple[List[Todo], List[Todo]]:
        from tests.generate_test_data import generate

        generate()

        w = Workspace.all()[2]
        t = w.todos[0]

        old_todos = t.siblings
        t.sort_siblings(field)
        new_descriptions = t.siblings

        return old_todos, new_descriptions

    def test_sort_pending(self):
        _, new = self._sort_before_and_after("pending")
        values_dict = {"completed": 3, "pending": 2, "overdue": 1}
        values = [values_dict[t.status] for t in new]

        self.assertEqual(values, sorted(values))

    def test_sort_description(self):
        old, new = self._sort_before_and_after("description")
        old.sort(key=lambda x: x.description)

        self.assertEqual(old, new)

    def test_sort_recurrence(self):
        old, new = self._sort_before_and_after("recurrence")
        has_recurrence = [t for t in old if t.recurrence]

        has_recurrence.sort(key=lambda x: x.recurrence)
        self.assertEqual(has_recurrence, new[: len(has_recurrence)])

    def test_sort_effort(self):
        old, new = self._sort_before_and_after("effort")
        old.sort(key=lambda x: x.effort)
        self.assertEqual(old, new)

    def test_sort_urgency(self):
        old, new = self._sort_before_and_after("urgency")
        old.sort(key=lambda x: x.urgency)
        self.assertEqual(old, new)

    def test_due(self):
        old, new = self._sort_before_and_after("due")
        has_due = [t for t in old if t.due]

        has_due.sort(key=lambda x: x.due)
        self.assertEqual(has_due, new[: len(has_due)])
