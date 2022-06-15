import yaml
from pathlib import Path

HOME = Path.home()
XDG_CONFIG = HOME / ".config"
CONFIG = XDG_CONFIG / "doit" / "config.yaml"

SAMPLE = Path(__file__).parent.absolute() / "example_config.yaml"


class Config:
    def __init__(self) -> None:
        self.check_files()

    def check_files(self):
        if not CONFIG.is_file():
            with open(SAMPLE, "r") as f:
                with open(CONFIG, "w") as stream:
                    stream.write(f.read())

    def load_config(self, part: str = "main") -> dict:
        with open(CONFIG, "r") as stream:
            try:
                return yaml.safe_load(stream)[part]
            except yaml.YAMLError:
                return {}
