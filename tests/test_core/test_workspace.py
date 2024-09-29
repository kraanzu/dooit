from sqlalchemy import select
from tests.test_core.core_base import CoreTestBase
from dooit.api import Workspace


class WorkspaceTest(CoreTestBase):
    def test_workspace_creation(self):
        for _ in range(5):
            w = Workspace()
            w.save()

        result = Workspace.all()
        self.assertEqual(len(result), 5)

    def test_siblings_by_creation(self):
        for _ in range(5):
            w = Workspace()
            w.save()

        workspace = Workspace.all()[0]

        assert workspace is not None
        self.assertEqual(len(workspace.siblings), 5)

    def test_sibling_methods(self):
        for _ in range(5):
            w = Workspace()
            w.save()

        workspace = Workspace.all()[0]

        assert workspace is not None

        siblings = workspace.siblings
        index_ids = [w.order_index for w in siblings]

        self.assertTrue(siblings[0].is_first_sibling())
        self.assertTrue(siblings[-1].is_last_sibling())
        self.assertEqual(index_ids, [0, 1, 2, 3, 4])

    def test_parent_kind(self):
        workspace1 = Workspace()
        workspace1.save()

        workspace2 = Workspace(parent_workspace=workspace1)
        workspace2.save()

        self.assertTrue(workspace2.has_same_parent_kind)

    def test_sibling_add(self):
        w1 = Workspace()
        w1.save()

        w2 = w1.add_sibling()
        w2.save()

        w = w1.add_sibling()
        self.assertEqual(len(w.siblings), 3)
        self.assertEqual(w.order_index, 1)

    def test_workspace_add(self):
        super_w = Workspace()
        super_w.save()

        super_w.add_workspace()
        w = super_w.add_workspace()

        self.assertEqual(len(w.siblings), 2)
        self.assertEqual(w.order_index, 1)

    def test_todo_add(self):
        super_w = Workspace()
        super_w.save()

        super_w.add_todo()
        todo = super_w.add_todo()

        self.assertEqual(len(todo.siblings), 2)
        self.assertEqual(todo.order_index, 1)

    def test_comparable_fields(self):
        fields = Workspace.comparable_fields()
        expected_fields = ["description"]
        self.assertEqual(fields, expected_fields)

    def test_nest_level(self):
        w = Workspace()
        self.assertEqual(w.nest_level, 0)

        w = w.add_workspace()
        self.assertEqual(w.nest_level, 1)

        w = w.add_workspace()
        self.assertEqual(w.nest_level, 2)

    def test_root(self):
        query = select(Workspace)
        workspaces = self.session.execute(query).scalars().all()

        self.assertEqual(len(workspaces), 0)
