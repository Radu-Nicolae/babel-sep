import tests.test_support as test
import babel.sep_coverage as sep


def main():
    test.test_lazy_proxy()
    test.test_catalog_merge_files()
    print(sep.get_coverage(2))
    print(f"Coverage percentage: {sep.coverage_percentage(2)}%")


if __name__ == "__main__":
    main()
