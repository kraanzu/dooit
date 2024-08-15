from sqlalchemy import Engine
from sqlalchemy.orm import Session
from ._vars import default_engine


class Manager:
    """
    Class for managing sqlalchemy sessions
    """

    def register_engine(self, engine: Engine = default_engine):
        from dooit.api import BaseModel

        if getattr(self, "engine", None):
            self.session.close()
            self.engine.dispose(close=True)
            del self.session

        BaseModel.metadata.create_all(bind=engine)
        self.engine = engine
        self.session = Session(engine)
        self.session.autoflush = False

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()

    def save(self, obj):
        self.session.add(obj)
        self.session.commit()


manager = Manager()
