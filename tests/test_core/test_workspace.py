import unittest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from dooit.api import BaseModel as Base
from dooit.api.workspace import Workspace


class TestWorkspace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        cls.session = Session(bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

    def test_workspace_session(self):
        w = Workspace()
        w.save(session=self.session)

        self.assertIn(w, self.session)

    def test_workspace_creation(self):
        for _ in range(5):
            w = Workspace()
            w.save(self.session)

        query = select(Workspace)
        result = self.session.execute(query).scalars().all()

        self.assertEqual(len(result), 5)

    # def test_workspace_siblings_by_creation(self):
    #     for _ in range(5):
    #         w = Workspace()
    #         w.save(self.session)
    #
    #     query = select(Workspace)
    #     workspace = self.session.execute(query).scalars().first()
    #
    #     assert workspace is not None
    #     self.assertEqual(len(workspace.get_siblings(session=self.session)), 5)
