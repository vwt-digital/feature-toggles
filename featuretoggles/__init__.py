import inspect
import os
from dataclasses import dataclass
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
        if self.creation_date and (date.today() - self.creation_date).days > self.max_lifetime:
            logger.warning(
                f"Feature toggle {self.name} has been in the code for over {self.max_lifetime} days:"
                f" ({(date.today() - self.creation_date).days} days)."
            )
        return self.value


class TogglesList:
    def __init__(self, document):
        if os.path.isfile(document):
            with open(document, 'r') as f:
                self._toggle_config = yaml.load(f, Loader=yaml.SafeLoader)
        else:
            self._toggle_config = yaml.load(document, Loader=yaml.SafeLoader)

        if not hasattr(self, '__annotations__'):
            raise Exception("No toggles are declared")

        not_declared = set(self._toggle_config) - set(self.__annotations__)
        if not_declared:
            raise Exception(f"The following toggles are not declared: {not_declared}")

        not_configured = set(self.__annotations__) - set(self._toggle_config)
        if not_configured:
            raise Exception(f"The following toggles are not configured: {not_configured}")

        for toggle in self._toggle_config:
            self.__setattr__(toggle, Toggle(**self._toggle_config.get(toggle)))

    def __getattribute__(self, attr):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        if not attr.startswith("_") and attr in self._toggle_config:
            logger.info(f"Checking toggle {attr} in {calframe[1][1]}:{calframe[1][2]} {calframe[1][3]}()")
        return super().__getattribute__(attr)
