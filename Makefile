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
	@isort . --force-single-line-imports > /dev/null
	@autoflake -r -i --remove-all-unused-imports --remove-unused-variables ./validatable/
	@isort . > /dev/null
	@black .


.PHONY: lint
lint:
	@flake8 validatable/ tests/
	@black --check .
	@isort --check .

.PHONY: install-testing
install-testing:
	@pip install tests/requirements-testing.txt

.PHONY: install-linting
install-linting:
	@pip install tests/requirements-linting.txt

.PHONY: install
install:
	@pip install -U pip
	@pip install -e .
	@pip install -r requirements-dev.txt

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