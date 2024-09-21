from dooit.ui.tui import Dooit

TEMP_CONN = "sqlite:///:memory:"
run_pilot = Dooit(connection_string=TEMP_CONN).run_test
