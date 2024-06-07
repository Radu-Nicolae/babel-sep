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
    #                               babel/support.py                            #
    # ------------------------------------------------------------------------- #
    SUPPORT = Entity("babel/support.py", (0, 5))
    LDGETTEXT = Entity("ldgettext", (3, 5), is_sub_entry=True)
    LDNGETTEXT = Entity("ldngettext", (6, 8), is_sub_entry=True)

    # ------------------------------------------------------------------------- #
    #                               babel/units.py                              #
    # ------------------------------------------------------------------------- #
    UNITS = Entity("babel/units.py", (0, 4))

    # ------------------------------------------------------------------------- #
    #                          babel/messages/checkers.py                       #
    # ------------------------------------------------------------------------- #
    CHECKERS = Entity("babel/messages/checkers.py", (0, 11))
    PARSE = Entity("_parse", (0, 5), is_sub_entry=True)
    COMPATIBLE = Entity("_compatible", (6, 11), is_sub_entry=True)
