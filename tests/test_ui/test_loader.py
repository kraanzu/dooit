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
