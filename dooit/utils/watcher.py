import os
import appdirs

DIR = appdirs.user_data_dir("dooit")
filename = os.path.join(DIR, "todo.yaml")


class Watcher:
    def __init__(self):
        self._cached_stamp = -1
        self.filename = filename

    def has_modified(self) -> bool:
        stamp = int(os.stat(self.filename).st_mtime)
        if stamp != self._cached_stamp:
            res = self._cached_stamp != -1
            self._cached_stamp = stamp
            return res

        return False
