class DooitThemeBase:
    _name: str = "dooit-base"

    # background colors
    background_1: str = "#2E3440"  # Darkest
    background_2: str = "#3B4252"  # Lighter
    background_3: str = "#434C5E"  # Lightest

    # foreground colors
    foreground_1: str = "#D8DEE9"  # Darkest
    foreground_2: str = "#E5E9F0"  # Lighter
    foreground_3: str = "#ECEFF4"  # Lightest

    # other colors
    red: str = "#BF616A"
    orange: str = "#D08770"
    yellow: str = "#EBCB8B"
    green: str = "#A3BE8C"
    blue: str = "#5E81AC"
    purple: str = "#B48EAD"
    magenta: str = "#B48EAD"
    cyan: str = "#8FBCBB"

    # accent colors
    primary: str = "#88C0D0"
    secondary: str = "#81A1C1"

    @classmethod
    def to_css(cls) -> str:
        css = f"""\
$background_1: {cls.background_1};
$background_2: {cls.background_2};
$background_3: {cls.background_3};

$foreground_1: {cls.foreground_1};
$foreground_2: {cls.foreground_2};
$foreground_3: {cls.foreground_3};

$red: {cls.red};
$orange: {cls.orange};
$yellow: {cls.yellow};
$green: {cls.green};
$blue: {cls.blue};
$purple: {cls.purple};
$magenta: {cls.magenta};

$primary: {cls.primary};
$secondary: {cls.secondary};
"""

        return css
