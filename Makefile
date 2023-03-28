default: test

clean: clean-build clean-pyc clean-installer
c: clean

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -f .coverage
	rm -f *.log

clean-installer:
	rm -fr output/
	rm -fr app.spec
	rm -f smb3_eh_manip.spec
	rm -f smb3_eh_manip.zip

clean-pyc: ## remove Python file artifacts
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +

init:
	pip install -r .

init-dev:
	pip install -r requirements_test.txt

pyinstaller: clean
	pyinstaller --noconfirm --onefile --console \
		-n smb3_eh_manip --uac-admin \
		app.py
	cp -r data/ dist/
	cp config.ini.sample dist/
	cp data/installer/*.dll dist/
	cp README.* dist/
	7z a smb3_eh_manip.zip dist/*
	7z rn smb3_eh_manip.zip dist smb3_eh_manip

run-autosplitter:
	python -m smb3_eh_manip.autosplitter

run-livesplit-client:
	python -m smb3_eh_manip.app.servers.livesplit_client

run-test:
	pytest --cov=smb3_eh_manip --cov-report term-missing tests/

run-main:
	python -m smb3_eh_manip.main

run-serial-server:
	python -m smb3_eh_manip.app.servers.serial_server

release-test: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypitest dist/*

release-prod: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*

release: run-test release-test release-prod clean

rsss: run-serial-server
m: run-main
main: init m
t: run-test
test: init-dev t
