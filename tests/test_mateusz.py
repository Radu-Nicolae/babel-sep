from babel.localtime import _helpers
import pytest
import pytz

def test_get_tzinfo_or_raise():

    """
    Test the _get_tzinfo_or_raise function in _helpers.py.
    Make sure that all types of parameters return the appropriate objects.
    """

    with pytest.raises(LookupError):
        _helpers._get_tzinfo_or_raise("Continent/City")

    tzinfo = _helpers._get_tzinfo_or_raise("America/New_York")
    assert tzinfo is not None
    assert tzinfo.zone == "America/New_York"


def test_get_tzinfo():
    pass

def test_get_tzinfo_from_file():
    pass
