# define VENV_NAME to use a specific virtual environment. It defaults to `env`.
VENV_NAME?=env
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=python
VENV =

# check if the VENV file exists
ifneq ("$(wildcard $(PVENV_ACTIVATE))","")
    VENV = venv
    PYTHON = ${VENV_NAME}/bin/python3
endif

default: docstyle flake8 test

venv: $(VENV_NAME)/bin/activate

test: $(VENV)
	${PYTHON} -m pytest test --cov=notecard

docstyle: $(VENV)
	${PYTHON} -m pydocstyle notecard/ examples/

flake8: $(VENV)
    # E722 Do not use bare except, specify exception instead https://www.flake8rules.com/rules/E722.html
    # F401 Module imported but unused   https://www.flake8rules.com/rules/F401.html
    # F403 'from module import *' used; unable to detect undefined names  https://www.flake8rules.com/rules/F403.html
    # W503 Line break occurred before a binary operator https://www.flake8rules.com/rules/W503.html
    # E501 Line too long (>79 characters) https://www.flake8rules.com/rules/E501.html
	${PYTHON} -m flake8 test/ notecard/ examples/ --count --ignore=E722,F401,F403,W503,E501 --show-source --statistics

coverage: $(VENV)
	${PYTHON} -m pytest test --doctest-modules --junitxml=junit/test-results.xml --cov=notecard --cov-report=xml --cov-report=html

run_build: $(VENV)
	${PYTHON} -m setup sdist bdist_wheel

deploy: $(VENV)
	${PYTHON} -m twine upload -r "pypi" --config-file .pypirc 'dist/*'

.PHONY: venv test coverage run_build deploy
