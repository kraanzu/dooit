from pathlib import Path
from platformdirs import user_cache_dir
from dooit.api.theme import DooitThemeBase
from uuid import uuid4

dooit_cache_path = Path(user_cache_dir("dooit"))

def generate_random_id():
    return uuid4().hex

class CssManager:
    css_file: Path = dooit_cache_path / "dooit.css"
    stylesheets: Path = dooit_cache_path / "stylesheets"

    def refresh_css(self):
        css = ""

        for sheet in self.stylesheets.iterdir():
            with open(sheet, "r") as f:
                css = css + "\n" + f.read()

        self.write(css)

    def set_theme(self, theme: DooitThemeBase):
        theme_file = self.stylesheets / "theme.css"

        with open(theme_file, "w") as f:
            f.write(theme.to_css())

        self.refresh_css()

    def inject_css(self, css: str) -> str:
        uuid = generate_random_id()
        css_file = self.stylesheets / f"{uuid}.css"

        with open(css_file, "w") as f:
            f.write(css)

        return uuid

    def uninject_css(self, _id: str) -> bool:
        css_file = self.stylesheets / f"{_id}.css"

        if not css_file.exists():
            return False

        css_file.unlink()
        self.refresh_css()
        return True

    def write(self, css: str):
        with open(self.css_file, "w") as f:
            f.write(css)
