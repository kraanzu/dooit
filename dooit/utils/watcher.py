import os
from dooit.utils.parser import TODO_DATA


class Watcher:
    """
    Watcher class for detecting todo data file changes
    """

    def __init__(self):
        self._cached_stamp = -1
        self.filename = TODO_DATA

    def has_modified(self) -> bool:
        """
        Checks if the file has modified since last cached time
        """

        stamp = os.stat(self.filename).st_mtime
        if abs(stamp - self._cached_stamp) >= 10**-6:
            res = self._cached_stamp != -1
            self._cached_stamp = stamp
            return res

        return False
