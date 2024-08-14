from dooit.api.workspace import Workspace
from tests.test_core._base import CoreTestBase


class TestModel(CoreTestBase):
    # Using Workspace as an example because Model is an abstract class

    def test_model_session(self):
        w = Workspace()
        w.save(session=self.session)
        self.assertIn(w, self.session)
