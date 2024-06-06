# [Software Engineering Processes] Coverage Measurement Tool

This file documents the entirety of the (self implemented) coverage measurement tool.
The tool is a manual instrumentation coverage measurement tool that allows the user to measure the coverage of a program
given the unit tests.

This tool depends on `pytest` and other dependencies to work correctly. See the [Dependencies](#dependencies) section
for more information.

## Table of Contents

- [Dependencies](#dependencies)
- [Entity Coverage](#entity-coverage)
    - [Registering Entities](#registering-entities)
- [Instrumentation](#instrumentation)
    - [Example Instrumentation](#example-instrumentation)
- [Functionality](#functionality)
    - [Example Program](#example-program)
    - [Example output](#example-output)
- [Extra functionality](#extra-functionality)
    - [Example Program](#example-program-1)

---

## Dependencies

This tool is developed in Python 3.12.3, thus any other version is not guaranteed to work.
Install the dependencies by running:

```bash
make sep_setup
```

---

## Entity Coverage

To solve the problem of manual instrument coverage testing, the covered program is split into entities.
Each entity might represent a file, a class, a function, or a method.

A file's coverage is absolute, meaning that its range of instrument identifiers starts at 0 and includes every other
interval for any other entity registered in the file.
Therefore, classes, functions and methods have entity tags that are marked with `is_sub_entry = True` in the **Entity**
class.

Sub-entries do not contribute to the total coverage calculation, as they are included in the parent entity's coverage.
This is marked in the final output with an `*` preceding the entity name.

### Registering Entities

When doing manual instrumentation, the user must register the entities in the coverage tool, in the  `program_entity.py`
file.
It contains an enumeration of all the entities in the program, with the following fields:

- `name`: The name of the entity. It represents the name of the file, class, function, or method.
- `id_range`: The ranges of instrument identifiers for the entity. It is a tuple of two integers, representing the
  starting and ending range of the entity.
- `is_sub_entry`: A boolean flag that indicates if the entity is a sub-entry of another entity.

Careful registration of entities is crucial for the correct calculation of coverage.

---

## Instrumentation

Coverage instrumentation is done by adding the following line at the beginning of each selected branch or statement to
be included in the coverage:

```python
coverage.instrument([ENTITY_FLAG_1, ENTITY_FLAG_2, ...], instrument_id)
```

The first parameter is a list of entity flags that the statement belongs to, and the second parameter is the instrument
identifier. It is crucial for the parameters of `instrument` to follow the following rules:

1. Only one non-sub-entry (`is_sub_entry = False`) entity flag is allowed in the list of entity flags.
2. In a given file, each instrument identifier must be unique and follow a count-by-one pattern, starting at the
   beginning of the file.
3. The entities must be registered in the `program_entity.py` file, and the instrument identifiers must be within the
   range of the entity.

### Example Instrumentation

```python
from coverage import instrument, CoverageEntity

instrument([CoverageEntity.UNITS], 0)
locale = Locale.parse(locale)
instrument([CoverageEntity.UNITS], 1)
unit = _find_unit_pattern(measurement_unit, locale=locale)
instrument([CoverageEntity.UNITS], 2)
if not unit:
    instrument([CoverageEntity.UNITS], 3)
    raise UnknownUnitError(unit=measurement_unit, locale=locale)

instrument([CoverageEntity.UNITS], 4)
return locale.unit_display_names.get(unit, {}).get(length)
```

---

## Functionality

Start by importing the coverage module:

```python
import coverage
```

Afterward, you can run all the tests to generate coverage data by executing `coverage.run()`.
Printing the data is simply done by calling `coverage.print_all()`.

### Example Program

```python
from coverage import run, print_all


def main():
    run()
    print_all()


if __name__ == "__main__":
    main()
```

### Example output

```
Running tests...
+------------------+-------+------+-------+
|       Name       | Stmts | Miss | Cover |
+------------------+-------+------+-------+
| babel/support.py |   2   |  1   |  66%  |
|  babel/units.py  |   5   |  0   | 100%  |
|      Total       |   7   |  1   |  87%  |
+------------------+-------+------+-------+
```

---

## Extra functionality

After executing `coverage.run()`, the user can extract information about given entities by
calling `get_coverage_data(entity)`.

The function has the following signature:

```python
def get_coverage_data(entity: CoverageEntity) -> dict[str, int or str]:
```

It takes as a parameter containing the entity (from the enum `CoverageEntity`) and returns a dictionary with the
following keys:

- `name` (str): The name of the entity.
- `reached` (int): The number of statements instrumented that were reached for the given entity.
- `missed` (int): The number of statements instrumented that were not reached for the given entity.
- `coverage` (str): The coverage percentage for the given entity, formatted as `[0-9]{1,2}%`.

### Example Program

```python
from coverage import run, get_coverage_data, CoverageEntity


def main():
    run()
    print(get_coverage_data(CoverageEntity.UNITS)["coverage"])


if __name__ == "__main__":
    main()
```

---
