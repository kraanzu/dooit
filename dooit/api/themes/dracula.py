from ..theme import DooitThemeBase


class Dracula(DooitThemeBase):
    background_1: str = "#282a36"  # Darkest
    background_2: str = "#44475a"  # Lighter
    background_3: str = "#5f637e"  # Lightest

    # foreground colors
    foreground_1: str = "#cccccc"  # Darkest
    foreground_2: str = "#e6e6e6"  # Lighter
    foreground_3: str = "#f8f8f2"  # Lightest

    # other colors
    red: str = "#ff5555"
    orange: str = "#ffb86c"
    yellow: str = "#f1fa8c"
    green: str = "#50fa7b"
    blue: str = "#8be9fd"
    purple: str = "#bd93f9"
    magenta: str = "#ff79c6"
    cyan: str = "#8be9fd"

    # accent colors
    primary: str = purple
    secondary: str = cyan
