import logging
import datetime
import pytest

from featuretoggles import TogglesList


def test_normal(caplog):
    caplog.set_level(logging.INFO)

    class ReleaseToggles(TogglesList):
        feature1: bool

    config = f"""
---
feature1:
    value: true
    name: New Thing Toggler
    description: This toggles the new thing on
    jira: DAN-123
    creation_date: {datetime.date.today():%Y-%m-%d}
    """
    toggles = ReleaseToggles(config)

    assert bool(toggles.feature1)
    assert "WARNING" not in caplog.text
    assert "Checking toggle feature1" in caplog.text


def test_lifetime_exceeded(caplog):
    caplog.set_level(logging.INFO)

    class ReleaseToggles(TogglesList):
        feature1: bool

    config = f"""
---
feature1:
    value: true
    name: New Thing Toggler
    description: This toggles the new thing on
    jira: DAN-123
    creation_date: {datetime.date.today() - datetime.timedelta(days=4):%Y-%m-%d}
    max_lifetime: 3
    """
    toggles = ReleaseToggles(config)

    assert bool(toggles.feature1)
    assert "Feature toggle New Thing Toggler has been in the code for over 3 days: (4 days)" in caplog.text
    assert "Checking toggle feature1" in caplog.text


def test_not_configured(caplog):
    caplog.set_level(logging.INFO)

    class ReleaseToggles(TogglesList):
        feature1: bool
        feature2: bool

    config = """
---
feature1: blank
    """

    with pytest.raises(Exception, match=r"The following toggles are not configured:.*"):
        ReleaseToggles(config)


def test_nothing_declared(caplog):
    caplog.set_level(logging.INFO)

    class ReleaseToggles(TogglesList):
        ...

    config = """
---
feature1: blank
    """

    with pytest.raises(Exception, match=r"No toggles are declared"):
        ReleaseToggles(config)


def test_not_declared(caplog):
    caplog.set_level(logging.INFO)

    class ReleaseToggles(TogglesList):
        feature1: bool

    config = """
---
feature1: blank
feature2: blank
    """

    with pytest.raises(Exception, match=r"The following toggles are not declared:.*"):
        ReleaseToggles(config)


def test_bad_config(caplog):
    caplog.set_level(logging.INFO)

    class ReleaseToggles(TogglesList):
        feature1: bool

    config = f"""
---
feature1:
    value: true
    description: This toggles the new thing on
    jira: DAN-123
    creation_date: {datetime.date.today():%Y-%m-%d}
    """

    with pytest.raises(Exception) as e:
        ReleaseToggles(config)
    assert "__init__() missing 1 required positional argument: 'name'" in str(e)
