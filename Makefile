# define VENV_NAME to use a specific virtual environment. It defaults to `env`.
VENV_NAME?=env
VENV_ACTIVATE=$(VENV_NAME)/bin/activate
PYTHON=python
# the target to activate the virtual environment. Only defined if it exists.

# check if the VENV file exists, if it does assume that's been made active
ifneq ("$(wildcard ${VENV_ACTIVATE})","")
	RUN_VENV_ACTIVATE=. ${VENV_ACTIVATE}
	PYTHON = ${VENV_NAME}/bin/python3
endif

default: precommit

precommit: docstyle flake8

test:
	${RUN_VENV_ACTIVATE}
	${PYTHON} -m pytest test --cov=notecard --ignore=test/hitl

docstyle:
	${RUN_VENV_ACTIVATE}
	${PYTHON} -m pydocstyle notecard/ examples/ mpy_board/

flake8:
	${RUN_VENV_ACTIVATE}
	# E722 Do not use bare except, specify exception instead https://www.flake8rules.com/rules/E722.html
	# F401 Module imported but unused   https://www.flake8rules.com/rules/F401.html
	# F403 'from module import *' used; unable to detect undefined names  https://www.flake8rules.com/rules/F403.html
	# W503 Line break occurred before a binary operator https://www.flake8rules.com/rules/W503.html
	# E501 Line too long (>79 characters) https://www.flake8rules.com/rules/E501.html
	${PYTHON} -m flake8 --exclude=notecard/md5.py test/ notecard/ examples/ mpy_board/ --count --ignore=E722,F401,F403,W503,E501,E502 --show-source --statistics

coverage:
	${RUN_VENV_ACTIVATE}
	${PYTHON} -m pytest test --ignore=test/hitl --doctest-modules --junitxml=junit/test-results.xml --cov=notecard --cov-report=xml --cov-report=html

run_build:
	${RUN_VENV_ACTIVATE}
	${PYTHON} -m setup sdist bdist_wheel

deploy:
	${RUN_VENV_ACTIVATE}
	${PYTHON} -m twine upload -r "pypi" --config-file .pypirc 'dist/*'

.PHONY: precommit venv test coverage run_build deploy
