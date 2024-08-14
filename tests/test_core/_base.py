from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dooit.api import BaseModel as Base


class CoreTestBase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        cls.session = Session(bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.session = Session(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def tearDown(self) -> None:
        self.session.rollback()
        self.session.close()
