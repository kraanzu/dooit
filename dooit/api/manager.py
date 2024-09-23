from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ._vars import DATABASE_CONN_STRING


class Manager:
    """
    Class for managing sqlalchemy sessions
    """

    def register_engine(self, conn: Optional[str] = None):
        from dooit.api import BaseModel

        conn = conn or DATABASE_CONN_STRING

        self.engine = create_engine(conn)
        self.session = Session(self.engine)
        self.session.autoflush = False

        BaseModel.metadata.create_all(bind=self.engine)

    def delete(self, obj):
        self.session.delete(obj)
        self.commit()

    def save(self, obj):
        self.session.add(obj)
        self.commit()

    def commit(self):
        self.session.commit()


manager = Manager()
