import pytest
from gudlift.routes import checkFormatPlaceRequired


def test_x():
    assert checkFormatPlaceRequired(0) is False
    assert checkFormatPlaceRequired(-10) is False
    assert checkFormatPlaceRequired(10) is True
