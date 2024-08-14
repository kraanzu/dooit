from sqlalchemy import select
from tests.test_core._base import CoreTestBase
from dooit.api import Workspace


class WorkspaceTest(CoreTestBase):
    def test_workspace_creation(self):
        for _ in range(5):
            w = Workspace()
            w.save(self.session)

        query = select(Workspace)
        result = self.session.execute(query).scalars().all()
        self.assertEqual(len(result), 5)

    def test_sibling_methods(self):
        for _ in range(5):
            w = Workspace()
            w.save(self.session)

        query = select(Workspace)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None

        siblings = workspace.get_siblings(session=self.session)
        index_ids = [w.order_index for w in siblings]
        self.assertEqual(index_ids, [1, 2, 3, 4, 5])
        self.assertTrue(siblings[0].is_first_sibling(session=self.session))
        self.assertTrue(siblings[-1].is_last_sibling(session=self.session))

    def test_workspace_siblings_by_creation(self):
        for _ in range(5):
            w = Workspace()
            w.save(self.session)

        query = select(Workspace)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None
        self.assertEqual(len(workspace.get_siblings(session=self.session)), 5)

    def test_parent_kind(self):
        workspace1 = Workspace()
        workspace1.save(self.session)

        workspace2 = Workspace(parent_workspace=workspace1)
        workspace2.save(self.session)

        self.assertTrue(workspace2.has_same_parent_kind)
