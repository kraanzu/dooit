from tests.test_ui.ui_base import run_pilot
from dooit.ui.tui import Dooit
from dooit.ui.api import loader
import tempfile
from pathlib import Path


async def test_loader():
    async with run_pilot() as pilot:
        app = pilot.app
        assert isinstance(app, Dooit)
        temp_folder = Path(tempfile.TemporaryDirectory().name)

        incorrect_path = temp_folder / "incorrect_path"
        assert not loader.load_file(app.api.plugin_manager, incorrect_path)

        incorrect_folder = temp_folder / "incorrect_folder"
        assert not loader.load_dir(app.api.plugin_manager, incorrect_path)

        subfolder = incorrect_folder / "subfolder"
        test_file = subfolder / "test_file.py"

        subfolder.mkdir(parents=True, exist_ok=True)
        test_file.touch()

        assert loader.load_dir(app.api.plugin_manager, incorrect_folder)
