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

format: isort black

flake8:
	@flake8 validatable/

check: flake8
	@black --check .
	@isort --check .
