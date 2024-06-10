from babel import support
from babel import Locale
from babel.util import FixedOffsetTimezone
import datetime


def test_fixed_offset_timezone():
    """
    Test the FixedOffsetTimezone class in util.py.
    Make sure that the class initializes
    """

    # 0 offset timezone
    offset = FixedOffsetTimezone(0)

    assert str(offset) == 'Etc/GMT+0'
    assert repr(offset) == '<FixedOffset "Etc/GMT+0" 0:00:00>'
    assert offset.utcoffset(datetime.datetime.now()) == datetime.timedelta(0)
    assert offset.tzname(datetime.datetime.now()) == 'Etc/GMT+0'
    assert offset.dst(datetime.datetime.now()) == datetime.timedelta(0)


def test_locales_to_names():
    """
    Test the _locales_to_names function in support.py.
    Make sure that all types of parameters return the appropriate array objects.
    """

    assert support._locales_to_names(None) is None
    assert support._locales_to_names(Locale('en')) == ['en']
    assert support._locales_to_names('en_US') == ['en_US']
