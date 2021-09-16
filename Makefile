SHELL := /bin/bash
.PHONY: check test cov

pipe: check test cov

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

test:
	@PYTHONPATH=.:./validatable coverage run -m py.test
lf:
	@PYTHONPATH=.:./validatable py.test --lf
cov:
	@coverage report -m

black:
	@black .

isort:
	@isort .

autoflake:
	@isort . --force-single-line-imports > /dev/null
	@autoflake -r -i --remove-all-unused-imports --remove-unused-variables ./validatable/
	@isort . > /dev/null

format: black autoflake

flake8:
	@flake8 validatable/

check: flake8
	@black --check .
	@isort --check .

c:
	@./scripts/commit.sh