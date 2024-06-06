test: import-cldr
	python ${PYTHON_TEST_FLAGS} -m pytest ${PYTEST_FLAGS}

clean: clean-cldr clean-pyc

import-cldr:
	python scripts/download_import_cldr.py

clean-cldr:
	rm -f babel/locale-data/*.dat
	rm -f babel/global.dat

clean-pyc:
	find . -name '*.pyc' -exec rm {} \;
	find . -name '__pycache__' -type d | xargs rm -rf

develop:
	pip install --editable .

tox-test:
	tox

setup_sep:
	virtualenv venv > /dev/null
	(. ./venv/bin/activate && pip install -r requirements.txt && export PYTHONPATH=$(realpath venv/lib/python3.12/site-packages/) && python setup.py import_cldr && pip install --editable .) > /dev/null 2>&1

sep_coverage:
	. ./venv/bin/activate && python3 sep_coverage.py



.PHONY: test develop tox-test clean-pyc clean-cldr import-cldr clean standalone-test
