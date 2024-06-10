import enum


class Entity:
    def __init__(self, name: str, id_range: tuple[int, int], is_sub_entry: bool = False) -> None:
        self.name = name
        self.id_range = id_range
        self.is_sub_entry = is_sub_entry


class CoverageEntity(enum.Enum):
    """
    Enum containing all the registered entities in the program.
    All entities are defined in the format:

    Entity(name, (start_line, end_line), is_sub_entry=False)
    name:           The name of the entity (file name, method name, etc.)
    start_line:     The beginning identifier number in the entity
    end_line:       The ending identifier number in the entity
    is_sub_entry:   True if the entity is not a file, but a sub-entry (e.g. a method)

    Extend this enum with new entities as needed. Ensure that the start_line and end_line
    values are correct for the entity. Otherwise, the coverage data will be incorrect.
    """

    # ------------------------------------------------------------------------- #
    #                               babel/dates.py                              #
    # ------------------------------------------------------------------------- #
    DATES = Entity("babel/dates.py", (0, 35))
    FORMAT_DATE = Entity("format_date", (0, 7), is_sub_entry=True)
    DATETIMEPATTERN_STR = Entity("DateTimePattern#str", (8, 9), is_sub_entry=True)

    GET_DATE = Entity("_get_time", (10, 22), is_sub_entry=True)
    GET_TIMEZONE = Entity("get_timezone", (23, 35), is_sub_entry=True)

    # ------------------------------------------------------------------------- #
    #                    babel/localtime/_helpers.py                            #
    # ------------------------------------------------------------------------- #

    HELPERS = Entity("babel/localtime/_helpers.py", (1,12))
    GETTZINFO = Entity("_get_tzinfo", (1, 4), is_sub_entry=True)
    GETTZINFOORRAISE = Entity("get_tzinfo_or_raise", (5, 8), is_sub_entry=True)
    GETTZINFOFROMFILE = Entity("get_tzinfo_from_file", (9, 12), is_sub_entry=True)

    # ------------------------------------------------------------------------- #
    #                    babel/util.py                                          #
    # ------------------------------------------------------------------------- #
    UTIL = Entity("babel/util.py", (0, 8))
    FIXED_OFFSET_TIMEZONE = Entity("FixedOffsetTimezone", (0, 8), is_sub_entry=True)
