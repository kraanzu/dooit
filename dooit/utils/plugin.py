from ..api.manager import Manager


class Plugin:
    ready: bool = False
    running: bool = False

    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    def commit(self):
        self.manager.commit()

    def is_ready(self) -> bool:
        return self.ready

    def pre_process(self) -> None:
        # All the pre processing stuff happens here
        # After it's done, mark `ready` param to True
        pass
        self.ready = True

    def run(self) -> bool:
        # Do your magic here!
        # Return True to call again else return False
        return False

    def run_on_exit(self) -> None:
        pass
