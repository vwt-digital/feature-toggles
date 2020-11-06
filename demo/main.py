import logging
from featuretoggles import TogglesList

logging.basicConfig(
    level=logging.INFO
)


class ReleaseToggles(TogglesList):
    feature1: bool
    feature2: bool


tl = ReleaseToggles('toggles.yaml')


def main():
    if tl.feature1:
        print("hoi")
    else:
        print("doei")


main()
