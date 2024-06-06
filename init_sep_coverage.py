import babel.sep_coverage as sep
import pytest


def test_coverage_A():
    LOWER_RANGE = 0
    UPPER_RANGE = 2
    range_ids = (LOWER_RANGE, UPPER_RANGE)

    pytest.main()
    print(sep.get_coverage(range_ids))
    print(f"Coverage percentage: {sep.coverage_percentage(range_ids)}%")


def main():
    test_coverage_A()


if __name__ == "__main__":
    main()
