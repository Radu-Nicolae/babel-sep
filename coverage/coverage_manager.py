from coverage.program_entity import CoverageEntity
from tabulate import tabulate
import pytest
import sys
import os

"""
Dictionary containing the coverage data for each entity.
An entity can be a module, class, function, or method.

The key is the entity and the value is a set of identifiers (integers).
The set contains the identifiers of the statements that were reached.
"""
code_coverage: dict[CoverageEntity, set[int]] = {entity: set() for entity in list(CoverageEntity)}


def instrument(entities: list[CoverageEntity], identifier: int) -> None:
    """
    Register the statement with a given identifier as covered (if reached).
    @param entities:    The entity tags that the identifier belongs to.
    @param              identifier: The identifier of the branch.
    """

    for entity in entities:
        # Error handle invalid entities and identifiers
        if entity not in code_coverage:
            raise ValueError(f"Entity {entity.value.name} is not supported")

        if identifier < entity.value.id_range[0] or identifier > entity.value.id_range[1]:
            raise ValueError(f"Identifier {identifier} is not in the range of {entity.value.name}")

        # Add the identifier to the coverage set
        # I.e. if instrument() is called, it means the statement is reached
        code_coverage[entity].add(identifier)


def get_unreachable_ids(entity: CoverageEntity) -> list[int]:
    """
    Get a list of unreachable statements (as identifiers) for a given entity.
    @param entity:  The entity to get the coverage for.
    @return:        A list of unreachable statements.
    """

    # Error handle invalid entities
    if entity not in code_coverage:
        raise ValueError(f"Entity {entity.value.name} is not supported")

    sorted_ids: list = sorted(code_coverage[entity])
    unaccessed_line_ids: list = []
    last_id: int = entity.value.id_range[0] - 1

    for instrument_id in sorted_ids:
        # If there are IDs skipped
        if instrument_id - last_id > 1:
            # Add all skipped IDs
            for i in range(last_id + 1, instrument_id):
                unaccessed_line_ids.append(i)

        # Update the last ID
        last_id = instrument_id

    # Add all skipped ids until the last instrumented line
    for i in range(last_id + 1, entity.value.id_range[1] + 1):
        unaccessed_line_ids.append(i)

    return unaccessed_line_ids


def coverage_percentage(entity: CoverageEntity) -> float:
    """
    Get the coverage percentage for a given entity.
    @param entity:  The entity to get the coverage percentage for.
    @return:        The coverage percentage (float, two decimal places).
    """

    # Error handle invalid entities
    if entity not in code_coverage:
        raise ValueError(f"Entity {entity.value.name} is not supported")

    total_lines_of_code = entity.value.id_range[1] - entity.value.id_range[0] + 1
    percentage = (1 - len(get_unreachable_ids(entity)) / total_lines_of_code) * 100
    return round(percentage, 2)


def get_coverage_data(entity: CoverageEntity) -> dict[str, int or str]:
    """
    Get the coverage data for a given entity.
    @param entity:  The entity to get the coverage data for.
    @return:        A dictionary containing the coverage data.
                    name:       The name of the entity.
                    reached:    The number of reached statements.
                    missed:     The number of missed statements.
                    coverage:   The coverage percentage (formatted).
    """

    # Error handle invalid entities
    if entity not in code_coverage:
        raise ValueError(f"Entity {entity.value.name} is not supported")

    total_statements: int = entity.value.id_range[1] - entity.value.id_range[0] + 1
    unreachable_ids: list[int] = get_unreachable_ids(entity)

    return {
        "name": entity.value.name,
        "reached": total_statements - len(unreachable_ids),
        "missed": len(unreachable_ids),
        "coverage": str(int(coverage_percentage(entity))) + "%"
    }


def get_total_data() -> dict[str, int or str]:
    """
    Get the total coverage data for all non sub-entry entities.
    @return:    A dictionary containing the total coverage data.
                name:       The name of the entity.
                reached:    The number of reached statements.
                missed:     The number of missed statements.
                coverage:   The coverage percentage (formatted).
    """

    total_coverage = 0
    total_statements = 0

    for entity in code_coverage.keys():
        # Ignore sub-entries when calculating the total coverage
        if entity.value.is_sub_entry:
            continue

        total_statements += entity.value.id_range[1] - entity.value.id_range[0] + 1
        total_coverage += len(get_unreachable_ids(entity))

    total_percentage = (1 - total_coverage / total_statements) * 100

    return {
        "name": "Total",
        "reached": total_statements - total_coverage,
        "missed": total_coverage,
        "coverage": str(int(total_percentage)) + "%"
    }


def run():
    """
    Run the tests to generate and collect coverage data.
    """

    print("Running tests...")

    # To mitigate the output of pytest
    # redirect the output to /dev/null
    with open(os.devnull, "w") as devnull:
        sys.stdout = devnull
        # Run all tests using pytest.
        pytest.main(["-q"])

    # Reset the output
    sys.stdout = sys.__stdout__


def print_all():
    """
    Print the coverage data for all entities in a tabular format.
    """

    HEADERS = ["Name", "Stmts", "Miss", "Cover"]
    data = []

    for entity in code_coverage.keys():
        entity_data = list(get_coverage_data(entity).values())

        # Mark sub-entries with an asterisk
        # * = does not contribute to the total coverage
        if entity.value.is_sub_entry:
            entity_data[0] = "* " + entity_data[0]

        data.append(entity_data)

    data.append(get_total_data().values())
    print(tabulate(data, headers=HEADERS, tablefmt="pretty"))
