from dooit.utils.parser import PLUGINS
from threading import Thread
import os
import sys
import importlib


def run_file(d, file_name):
    full_path = os.path.join(d, file_name)
    sys.path.append(d)
    sys.path.append(full_path)
    importlib.import_module(file_name[:-3])


class Plug:
    @classmethod
    def entry(cls):
        for directory, _, filelist in os.walk(PLUGINS):
            for f in filelist:
                if f.endswith("entry.py"):
                    Thread(
                        target=run_file,
                        args=(
                            directory,
                            f,
                        ),
                        daemon=True,
                    ).start()

    @classmethod
    def exit(cls):
        for directory, _, filelist in os.walk(PLUGINS):
            for f in filelist:
                if f.endswith("exit.py"):
                    Thread(
                        target=run_file,
                        args=(
                            directory,
                            f,
                        ),
                        daemon=True,
                    ).start()
