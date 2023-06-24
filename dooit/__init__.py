import argparse
from importlib.metadata import version
from .ui.tui import Dooit
import asyncio


from .Tests import Test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("-t", "--test", help="Make test", action="store_true", default=False)
    args = parser.parse_args()

    if args.version:
        ver = version("dooit")
        print(f"dooit - {ver}")
    elif args.test:
        # Create a new event loop
        loop = asyncio.new_event_loop()

        # Set the new event loop as the current event loop
        asyncio.set_event_loop(loop)

        # Create a task for Test.run()
        test_task = loop.create_task(Test.run())

        # Gather the tasks and run them concurrently
        tasks = asyncio.gather(test_task)

        try:
            loop.run_until_complete(tasks)
        except KeyboardInterrupt:
            tasks.cancel()  # Cancel the tasks on keyboard interrupt
            loop.run_until_complete(tasks)

        # Cancel the set_interval task if it's still pending
        for task in asyncio.all_tasks(loop):
            if task.get_name() == 'set_interval#1':
                task.cancel()

        # Close the event loop
        loop.close()

    else:
        Dooit().run()
