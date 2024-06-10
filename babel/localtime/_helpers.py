try:
    import pytz
    from sep_coverage import instrument, CoverageEntity
except ModuleNotFoundError:
    pytz = None
    import zoneinfo

def _get_tzinfo(tzenv: str):
    """
    Get the tzinfo from `zoneinfo` or `pytz`
    
    :param tzenv: timezone in the form of Continent/City
    :return: tzinfo object or None if not found
    """
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 1)
    if pytz:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 2)
        try:
            return pytz.timezone(tzenv)
        except pytz.UnknownTimeZoneError:
            pass
    else:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 3)
        try:
            return zoneinfo.ZoneInfo(tzenv)
        except zoneinfo.ZoneInfoNotFoundError:
            pass
    
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFO], 4)
    return None

def _get_tzinfo_or_raise(tzenv: str):
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 5)
    tzinfo = _get_tzinfo(tzenv)
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 6)
    if tzinfo is None:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 7)
        raise LookupError(
            f"Can not find timezone {tzenv}. \n"
            "Timezone names are generally in the form `Continent/City`.",
        )
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOORRAISE], 8)
    return tzinfo


def _get_tzinfo_from_file(tzfilename: str):
    instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOFROMFILE], 9)
    
    with open(tzfilename, 'rb') as tzfile:
        instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOFROMFILE], 10)

        if pytz:
            instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOFROMFILE], 11)
            return pytz.tzfile.build_tzinfo('local', tzfile)
        else:
            instrument([CoverageEntity.HELPERS, CoverageEntity.GETTZINFOFROMFILE], 12)
            return zoneinfo.ZoneInfo.from_file(tzfile)
