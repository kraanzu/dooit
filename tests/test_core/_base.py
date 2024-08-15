from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dooit.api import manager

TEMP_ENGINE = create_engine("sqlite:///:memory:")


class CoreTestBase(TestCase):

    @classmethod
    def setUpClass(cls):
        manager.register_engine(TEMP_ENGINE)

    def setUp(self):
        manager.register_engine(TEMP_ENGINE)

    def tearDown(self) -> None:
        manager.session.rollback()
        manager.session.close()

    @property
    def session(self) -> Session:
        return manager.session
