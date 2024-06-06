code_set = set()


def instrument(id):
    code_set.add(id)


"""
....
@param max_instrument


"""


def get_coverage(max_instrument):
    list_sorted = sorted(code_set)
    unaccessed_lines = []
    last_item = -1

    for item in list_sorted:
        # If no ID was skipped
        if item - last_item == 1:
            for i in range(last_item + 1, item):
                unaccessed_lines.append(i)
            continue

        last_item = item

    for i in range(last_item + 1, max_instrument + 1):
        unaccessed_lines.append(i)

    return unaccessed_lines


"""
Computes the coverage percentage of the instrumented code.
@param max_instrument: The maximum instrumented line ID for the code.
@return: The coverage percentage as a floating point [0.0, 100.0].
"""


def coverage_percentage(max_instrument):
    total_lines_of_code = max_instrument + 1
    percentage = (1 - len(get_coverage(max_instrument)) / total_lines_of_code) * 100
    return round(percentage, 2)
