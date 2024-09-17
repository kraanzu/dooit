from unittest import TestCase
from sqlalchemy.orm import Session
from dooit.api import manager

TEMP_CONN = "sqlite:///:memory:"


class CoreTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        manager.register_engine(TEMP_CONN)

    def setUp(self):
        manager.register_engine(TEMP_CONN)

    def tearDown(self) -> None:
        manager.session.rollback()
        manager.session.close()

    @property
    def session(self) -> Session:
        return manager.session
