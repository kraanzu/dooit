from typing import Generic, TypeVar
from dooit.api.model import DooitModel
from dooit.ui.widgets.renderers.base_renderer import ModelType
from ._input import Input

ModelType = TypeVar("ModelType", bound=DooitModel)


class SimpleInput(Input, Generic[ModelType]):
    """
    A simple single line Text Input widget
    """

    _cursor_pos: int = 0
    _cursor: str = "|"

    def __init__(self, model: ModelType) -> None:
        super().__init__()

        self.model = model
        self.value = getattr(model, self._property)
        self._cursor_pos = len(self.value)

    @property
    def _property(self) -> str:
        return self.__class__.__name__.lower()

    def reset(self) -> str:
        self.value = getattr(self.model, self._property)
        self._cursor_pos = len(self.value)
        return self.value

    def stop_edit(self, cancel: bool = False) -> None:
        super().stop_edit()

        if not cancel:
            setattr(self.model, self._property, self.value)
            self.model.save()
        else:
            self.reset()

    def cancel_edit(self) -> None:
        return self.stop_edit(cancel=True)

    def keypress(self, key: str) -> None:
        super().keypress(key)

        if key == "escape":
            self.stop_edit()
