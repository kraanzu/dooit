from sqlalchemy import select
from dooit.api.workspace import Workspace
from tests.test_core._base import CoreTestBase, manager


class TestModel(CoreTestBase):
    # Using Workspace as an example because Model is an abstract class

    def test_model_session(self):
        w = Workspace()
        w.save()
        # self.assertIn(w, manager.session)

    def test_shifts(self):
        for _ in range(5):
            w = Workspace()
            w.save()

        query = (
            select(Workspace)
            .where(Workspace.is_root == False)
            .order_by(Workspace.order_index)
        )
        workspace = self.session.execute(query).scalars().all()[0]

        assert workspace is not None

        siblings = workspace.siblings
        self.assertTrue(workspace.is_first_sibling())

        workspace.shift_down()
        siblings = workspace.siblings
        self.assertEqual(siblings[1].id, workspace.id)
