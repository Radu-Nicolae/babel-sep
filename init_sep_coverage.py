import babel.sep_coverage as sep
import pytest


def main():
    pytest.main()
    print(sep.get_coverage(2))
    print(f"Coverage percentage: {sep.coverage_percentage(2)}%")


if __name__ == "__main__":
    main()
