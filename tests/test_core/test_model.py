from sqlalchemy import select
from dooit.api.workspace import Workspace
from tests.test_core._base import CoreTestBase


class TestModel(CoreTestBase):
    # Using Workspace as an example because Model is an abstract class

    def test_model_session(self):
        w = Workspace()
        w.save(session=self.session)
        self.assertIn(w, self.session)

    def test_shifts(self):
        for _ in range(5):
            w = Workspace()
            w.save(session=self.session)

        query = select(Workspace).order_by(Workspace.order_index)
        workspace = self.session.execute(query).scalars().first()

        assert workspace is not None

        siblings = workspace.get_siblings(session=self.session)
        self.assertTrue(siblings[0].is_first_sibling(session=self.session))

        workspace.shift_down(session=self.session)
        siblings = workspace.get_siblings(session=self.session)
        self.assertEqual(siblings[1], workspace)
