# Use pipenv for virtual environment management
PYTHON=python3

default: precommit

precommit: docstyle flake8

test:
	pipenv run pytest test --cov=notecard --ignore=test/hitl

docstyle:
	pipenv run pydocstyle notecard/ examples/ mpy_board/

flake8:
	# E722 Do not use bare except, specify exception instead https://www.flake8rules.com/rules/E722.html
	# F401 Module imported but unused   https://www.flake8rules.com/rules/F401.html
	# F403 'from module import *' used; unable to detect undefined names  https://www.flake8rules.com/rules/F403.html
	# W503 Line break occurred before a binary operator https://www.flake8rules.com/rules/W503.html
	# E501 Line too long (>79 characters) https://www.flake8rules.com/rules/E501.html
	pipenv run flake8 --exclude=notecard/md5.py test/ notecard/ examples/ mpy_board/ --count --ignore=E722,F401,F403,W503,E501,E502 --show-source --statistics

coverage:
	pipenv run pytest test --ignore=test/hitl --doctest-modules --junitxml=junit/test-results.xml --cov=notecard --cov-report=xml --cov-report=html

run_build:
	pipenv run python -m build

deploy:
	pipenv run python -m twine upload -r "pypi" --config-file .pypirc 'dist/*'

generate-api-docs:
	# Install required dependencies if not present
	pipenv install doxypypy
	# Generate documentation
	doxygen Doxyfile
	moxygen --output docs/api.md docs/xml

.PHONY: precommit test coverage run_build deploy generate-api-docs
