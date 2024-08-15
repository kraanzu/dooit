from tests.test_core._base import CoreTestBase
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
        self.assertEqual(index_ids, [1, 2, 3, 4, 5])

    def test_parent_kind(self):
        workspace1 = Workspace()
        workspace1.save()

        workspace2 = Workspace(parent_workspace=workspace1)
        workspace2.save()

        self.assertTrue(workspace2.has_same_parent_kind)
