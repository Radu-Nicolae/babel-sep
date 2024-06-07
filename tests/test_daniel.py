from babel import support
from babel import Locale


def test_locales_to_names():
    """
    Test the _locales_to_names function in support.py.
    Make sure that all types of parameters return the appropriate array objects.
    """

    assert support._locales_to_names(None) is None
    assert support._locales_to_names(Locale('en')) == ['en']
    assert support._locales_to_names('en_US') == ['en_US']
