SHELL := /bin/bash

.PHONY: help
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: test
test:
	@PYTHONPATH=.:./validatable coverage run -m py.test

.PHONY: cov
cov:
	@coverage report -m

.PHONY: format
format:
	@isort validatable tests --force-single-line-imports > /dev/null
	@autoflake -r -i --remove-all-unused-imports --remove-unused-variables validatable tests
	@isort validatable tests > /dev/null
	@black validatable tests


.PHONY: lint
lint:
	@flake8 validatable/ tests/
	@isort --check --diff validatable tests
	@black --check --diff validatable tests

.PHONY: install-testing
install-testing:
	@pip install -r tests/requirements-testing.txt

.PHONY: install-linting
install-linting:
	@pip install -r tests/requirements-linting.txt

.PHONY: install
install: install-testing
	@pip install -e .

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -f validatable/*.c validatable/*.so
	python setup.py clean
	rm -rf codecov.sh
	rm -rf coverage.xml