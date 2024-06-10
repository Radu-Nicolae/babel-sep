from babel.localtime import _helpers
import pytest
import pytest
import zoneinfo as zoneinfo

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

    _helpers.zoneinfo = zoneinfo
    _helpers.pytz = None
    tzenv = "Continent/City"
    assert _helpers._get_tzinfo(tzenv) is None
     
def test_get_tzinfo_from_file():
    
    with pytest.raises(FileNotFoundError):
        _helpers._get_tzinfo_from_file("tzfilename")
    
    with open("example.txt", 'w') as f:
        f.write("America/New_York")

    with pytest.raises(ValueError):
        _helpers._get_tzinfo_from_file("example.txt")

    _helpers.pytz = True
    with pytest.raises(AttributeError):
        _helpers._get_tzinfo_from_file("example.txt")
  