from dooit.ui.tui import Dooit

TEMP_CONN = "sqlite:///:memory:"
base_app = Dooit(connection_string=TEMP_CONN)


# class UITestBase(IsolatedAsyncioTestCase):
#     pilot: Pilot
#
#     async def asyncSetupClass(self):
#         async with Dooit(connection_string=TEMP_CONN).run_test() as pilot:
#             self.pilot = pilot
#
#     async def asyncSetup(self):
#         async with Dooit(connection_string=TEMP_CONN).run_test() as pilot:
#             self.pilot = pilot
#
#     def tearDown(self) -> None:
#         manager.session.rollback()
#         manager.session.close()
