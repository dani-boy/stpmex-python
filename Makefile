SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON=python3.7


default: install

venv:
		$(PYTHON) -m venv --prompt stpmex venv
		source venv/bin/activate
		pip install --quiet --upgrade pip

clean:
		find . -name '__pycache__' -exec rm -r "{}" +
		find . -name '*.pyc' -delete
		find . -name '*~' -delete

install: venv
		pip install --quiet --upgrade -r requirements.txt

install-dev: install
		pip install --quiet --upgrade -r requirements-dev.txt

test: lint
		pytest -v tests.py

lint:
		pycodestyle stpmex setup.py

