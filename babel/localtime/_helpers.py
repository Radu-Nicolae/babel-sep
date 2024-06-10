try:
    import pytz
    import sep_coverage
    from sep_coverage import instrument, CoverageEntity
    instrument([CoverageEntity.HELPERS], 0)
except ModuleNotFoundError:
    instrument([CoverageEntity.HELPERS], 1)
    pytz = None
    import zoneinfo
    instrument([CoverageEntity.HELPERS], 2)


def _get_tzinfo(tzenv: str):
    """Get the tzinfo from `zoneinfo` or `pytz`
    
    :param tzenv: timezone in the form of Continent/City
    :return: tzinfo object or None if not found
    """
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 3)
    if pytz:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 4)
        try:
            return pytz.timezone(tzenv)
        except pytz.UnknownTimeZoneError:
            pass
    else:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 5)
        try:
            return zoneinfo.ZoneInfo(tzenv)
        except zoneinfo.ZoneInfoNotFoundError:
            pass
    
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 6)
    return None

def _get_tzinfo_or_raise(tzenv: str):
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 7)
    tzinfo = _get_tzinfo(tzenv)
    if tzinfo is None:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 8)
        raise LookupError(
            f"Can not find timezone {tzenv}. \n"
            "Timezone names are generally in the form `Continent/City`.",
        )
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 9)
    return tzinfo


def _get_tzinfo_from_file(tzfilename: str):
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 10)
    
    with open(tzfilename, 'rb') as tzfile:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 11)

        if pytz:
            instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 12)

            return pytz.tzfile.build_tzinfo('local', tzfile)
        else:
            return zoneinfo.ZoneInfo.from_file(tzfile)
