from dooit.ui.tui import Dooit

TEMP_CONN = "sqlite:///:memory:"

def run_pilot():
    return Dooit(connection_string=TEMP_CONN).run_test()
