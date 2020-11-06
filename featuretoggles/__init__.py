import inspect
from dataclasses import dataclass, asdict
from datetime import date

import yaml

import logging

logger = logging.getLogger("Feature Toggles")


@dataclass(frozen=True)
class Toggle:
    value: bool
    name: str
    creation_date: date
    jira: str
    description: str = ""
    max_lifetime: int = 14

    def __bool__(self):
        if self.creation_date and (date.today() - self.creation_date).days > 14:
            logger.warning(
                f"Feature toggle {self.name} has been in the code for over {self.max_lifetime} days:"
                f" ({(date.today() - self.creation_date).days} days)."
            )
        return self.value

    def to_dict(self):
        return asdict(self)


class TogglesList:
    def __init__(self, file_name):
        with open(file_name, 'r') as f:
            self._toggle_config = yaml.load(f, Loader=yaml.SafeLoader)

        for toggle in self._toggle_config:
            if toggle not in self.__annotations__:
                raise Exception(f"{toggle} is not defined")
            else:
                self.__setattr__(toggle, Toggle(**self._toggle_config.get(toggle)))

    def __getattribute__(self, attr):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        if not attr.startswith("_") and attr in self._toggle_config:
            logger.info(f"Checking toggle {attr} in {calframe[1][1]}:{calframe[1][2]} {calframe[1][3]}()")
        return super().__getattribute__(attr)
