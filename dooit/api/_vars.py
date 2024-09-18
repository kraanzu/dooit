from pathlib import Path
from platformdirs import user_data_dir

# ROOT_FOLDER = Path(__file__).parent.parent.parent.absolute()  # local db file for testing

ROOT_FOLDER = Path(user_data_dir("dooit"))
DATABASE_FILE = ROOT_FOLDER / "dooit.db"
DATABASE_CONN_STRING = f"sqlite:////{DATABASE_FILE}"
