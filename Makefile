default: test

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

init:
	pip install -r .

init-dev:
	pip install -r requirements_test.txt

run-test:
	pytest --flake8 --black --cov=smb3_eh_manip --cov-report term-missing tests/

run-main:
	python -m smb3_eh_manip.main

release-test: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypitest dist/*

release-prod: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*

release: run-test release-test release-prod clean

m: run-main
main: init m
t: run-test
test: init-dev t
