VENV_NAME?=env
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

default: test

venv: $(VENV_NAME)/bin/activate

test: venv
	${PYTHON} -m pydocstyle notecard/ examples/
	${PYTHON} -m flake8 test/ notecard/ examples/ --count --ignore=E722,F401,F403,W503,E501 --show-source --statistics
	${PYTHON} -m pytest test --cov=notecard

coverage: venv
	${PYTHON} -m pytest test --doctest-modules --junitxml=junit/test-results.xml --cov=notecard --cov-report=xml --cov-report=html

run_build:
	${PYTHON} -m setup sdist bdist_wheel

deploy:
	${PYTHON} -m twine upload -r "pypi" --config-file .pypirc 'dist/*'

.PHONY: env test coverage run_build deploy
