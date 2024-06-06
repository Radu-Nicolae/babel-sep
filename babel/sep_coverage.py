code_set: set = set()

"""
Instrument a line of code with a unique ID =
Register the ID in a set, marking that line 
of code as reached during execution.
"""


def instrument(identifier: int) -> None:
    code_set.add(identifier)


"""
Create a list of all instrumented lines of code that are never
reached during execution.

@param max_instrument: The maximum instrumented line ID for the code.
@return 
"""


def get_coverage(max_instrument_id: int) -> list[int]:
    sorted_ids = sorted(code_set)
    unaccessed_line_ids : list = []
    last_id = -1

    for instrument_id in sorted_ids:
        # If no ID was skipped
        if instrument_id - last_id == 1:
            # Add all skipped IDs
            for i in range(last_id + 1, instrument_id):
                unaccessed_line_ids.append(i)
            continue

        last_id = instrument_id

    # Add all skipped ids until the last instrumented line
    for i in range(last_id + 1, max_instrument_id + 1):
        unaccessed_line_ids.append(i)

    return unaccessed_line_ids


"""
Computes the coverage percentage of the instrumented code.
@param max_instrument: The maximum instrumented line ID for the code.
@return: The coverage percentage as a floating point [0.0, 100.0].
"""


def coverage_percentage(max_instrument):
    total_lines_of_code = max_instrument + 1
    percentage = (1 - len(get_coverage(max_instrument)) / total_lines_of_code) * 100
    return round(percentage, 2)
