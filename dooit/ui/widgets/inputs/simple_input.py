from dooit.ui.widgets.renderers.base_renderer import ModelType
from ._input import Input


class SimpleInput(Input):
    """
    A simple single line Text Input widget
    """

    _cursor_position: int = 0
    _cursor: str = "|"

    def __init__(self, model: ModelType) -> None:
        self.model = model
        self.value = getattr(model, self._property)
        self._cursor_position = len(self.value)
        super().__init__()

    @property
    def _property(self) -> str:
        return self.__class__.__name__.lower()

    def refresh_value(self) -> str:
        self.value = getattr(self.model, self._property)
        return self.value

    def stop_edit(self, cancel: bool = False) -> None:
        super().stop_edit()

        if not cancel:
            setattr(self.model, self._property, self.value)
            self.model.save()
        else:
            value = self.refresh_value()

        self.refresh_value()

    def cancel_edit(self) -> None:
        return self.stop_edit(cancel=True)

    def keypress(self, key: str) -> None:
        super().keypress(key)

        if key == "escape":
            if True:
                self.stop_edit()
            else:
                self.cancel_edit()
