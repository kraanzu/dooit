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

    def test_workspace_siblings_by_creation(self):
        for _ in range(5):
            w = Workspace()
            w.save(self.session)

        query = select(Workspace)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None
        self.assertEqual(len(workspace.get_siblings(session=self.session)), 5)
