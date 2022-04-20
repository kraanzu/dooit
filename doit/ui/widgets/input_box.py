from rich.text import Text
from textual_extras.widgets import TextInput


class InputBox(TextInput):
    """
    Custom Input Box without Borders
    """

    def render_panel(self, text=Text):
        return text


if __name__ == "__main__":

    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(InputBox(), InputBox())

    MyApp.run()
