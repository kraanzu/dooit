import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ._vars import DATABASE_CONN_STRING


class Manager:
    """
    Class for managing sqlalchemy sessions
    """

    def connect(self, conn: Optional[str] = None):
        from dooit.api import BaseModel

        conn = conn or DATABASE_CONN_STRING

        self.engine = create_engine(conn)
        self.session = Session(self.engine)
        # self.session.autoflush = False

        BaseModel.metadata.create_all(bind=self.engine)
        self._db_last_modified = self._get_db_last_modified()

    def _get_db_last_modified(self) -> Optional[float]:
        database = self.engine.url.database
        assert database is not None

        try:
            return os.path.getmtime(database)
        except OSError:
            return None

    def has_changed(self) -> bool:
        current_last_modified = self._get_db_last_modified()
        if current_last_modified and self._db_last_modified != current_last_modified:
            self._db_last_modified = current_last_modified
            manager.session.expire_all()
            return True
        return False

    def delete(self, obj):
        self.session.delete(obj)
        self.commit()

    def save(self, obj):
        self.session.add(obj)
        self.commit()

    def commit(self):
        self.session.commit()
        self._db_last_modified = self._get_db_last_modified()


manager = Manager()
