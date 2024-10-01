from pathlib import Path
from dooit.api.manager import Manager
from dooit.api.workspace import Workspace
from tests.test_core.core_base import CoreTestBase
import tempfile


class TestSync(CoreTestBase):
    def test_sync(self):
        # create a temporary folder
        temp_folder = tempfile.TemporaryDirectory(delete=False)
        temp_db = Path(temp_folder.name) / "dooit1.db"
        TEMP_CONN = f"sqlite:////{temp_db}"

        manager1 = Manager()
        manager2 = Manager()

        manager1.register_engine(TEMP_CONN)
        manager2.register_engine(TEMP_CONN)

        w = Workspace(description="test")
        manager1.save(w)

        self.assertFalse(manager1.has_changed())
        self.assertTrue(manager2.has_changed())

        temp_folder.cleanup()
