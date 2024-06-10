import pytest
import babel.dates as dates
from babel.localtime._unix import _get_localzone
import datetime

def test_get_timezone():
    LOCALTZ = _get_localzone()
    assert dates.get_timezone() == LOCALTZ

    UNKNOWN_TZ = 'unknown'
    with pytest.raises(LookupError):
        dates.get_timezone(UNKNOWN_TZ)

def test_get_time():
    UTC = datetime.timezone.utc

    assert isinstance(dates._get_time(None), datetime.time)
    assert dates._get_time(None).tzinfo == UTC
    
    now = datetime.datetime.now(tz=UTC)
    ts = datetime.datetime.timestamp(now)

    assert dates._get_time(ts) == now.time().replace(tzinfo=UTC)

