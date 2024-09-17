from tests.test_ui._base import run_pilot


async def test_startup():
    async with run_pilot() as pilot:
        assert pilot.app.is_running
