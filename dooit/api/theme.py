class DooitThemeBase:
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
    pink: str = "#B48EAD"  # Nord doesn't have a distinct pink, using purple
    gray: str = "#4C566A"

    # accent colors
    primary: str = "#88C0D0"
    secondary: str = "#81A1C1"

    def to_css(self) -> str:
        css = f"""\
$background_1: {self.background_1};
$background_2: {self.background_2};
$background_3: {self.background_3};

$foreground_1: {self.foreground_1};
$foreground_2: {self.foreground_2};
$foreground_3: {self.foreground_3};

$red: {self.red};
$orange: {self.orange};
$yellow: {self.yellow};
$green: {self.green};
$blue: {self.blue};
$purple: {self.purple};
$pink: {self.pink};
$gray: {self.gray};

$primary: {self.primary};
$secondary: {self.secondary};
"""

        return css
