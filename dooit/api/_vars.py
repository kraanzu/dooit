from pathlib import Path
from sqlalchemy import create_engine
from appdirs import user_data_dir
from sqlalchemy.orm import Session


ROOT_FOLDER = Path(user_data_dir("dooit"))
ROOT_FOLDER = Path(__file__).parent.parent.parent.absolute() # TODO: remove this line

DATABASE_FILE = ROOT_FOLDER / "dooit.db"
DATABASE_CONN_STRING = f"sqlite:////{DATABASE_FILE}"

default_engine = create_engine(DATABASE_CONN_STRING, echo=False)
default_session = Session(default_engine)
