from dooit.api.workspace import Workspace
from tests.test_core._base import CoreTestBase


class TestModel(CoreTestBase):
    # Using Workspace as an example because Model is an abstract class

    def test_creation_and_deletion(self):
        w = Workspace()
        w.save()
        self.assertEqual(len(Workspace.all()), 1)

        w.drop()
        self.assertEqual(len(Workspace.all()), 0)

    def test_shifts(self):
        for _ in range(5):
            w = Workspace()
            w.save()

        workspace = Workspace.all()[0]

        assert workspace is not None

        siblings = workspace.siblings
        self.assertTrue(workspace.is_first_sibling())

        workspace.shift_down()
        siblings = workspace.siblings
        self.assertEqual(siblings[1].id, workspace.id)
