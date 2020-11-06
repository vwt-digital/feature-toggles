import logging
from featuretoggles import TogglesList

logging.basicConfig(
    level=logging.INFO
)


class ReleaseToggles(TogglesList):
    feature1: bool
    feature2: bool


toggles = ReleaseToggles('toggles.yaml')


def main():
    if toggles.feature1:
        print("Feature One Activated")
    else:
        print("Feature One Deactivated")


main()
