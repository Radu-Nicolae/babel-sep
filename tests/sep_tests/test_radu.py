from datetime import datetime

import babel.dates as dates

def test_format_date():
    assert dates.format_date(locale="en") == datetime.now().strftime("%b %-d, %Y")


def test_datetimepattern_str():
    date_time_pattern = dates.DateTimePattern(pattern="yyyy-MM-dd", format="long")
    assert str(date_time_pattern) == "yyyy-MM-dd"

