from ..api.manager import Manager


class Plugin:
    ready: bool = False

    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    def is_ready(self) -> bool:
        return self.ready

    def refresh(self) -> None:
        self.manager.refresh_data()

    def pre_process(self) -> None:
        # All the pre processing stuff happens here
        # After it's done, mark `ready` param to True
        pass

    def run(self) -> bool:
        # Do your magic here!
        # Return True to call again else return False
        raise NotImplemented

    def run_on_exit(self) -> None:
        pass
