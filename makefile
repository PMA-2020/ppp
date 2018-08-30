PYTHON=python3
SRC=./pmix/
TEST=./test/

.PHONY: lint tags ltags test all lint_all codestyle docstyle lint_src \
lint_test doctest doc docs code linters_all code_src code_test doc_src \
doc_test paper build dist pypi_push_test pypi_push pypi_test pip_test pypi \
pip demo

# Batched Commands
# - Code & Style Linters
all: linters_all test_all
lint: lint_src code_src doc_src
linters_all: doc code lint_all

# Pylint Only
PYLINT_BASE =${PYTHON} -m pylint --output-format=colorized --reports=n
lint_all: lint_src lint_test
lint_src:
	${PYLINT_BASE} ${SRC}
lint_test:
	${PYLINT_BASE} ${TEST}

# PyCodeStyle Only
PYCODESTYLE_BASE=${PYTHON} -m pycodestyle
codestyle: codestyle_src codestyle_test
code_src: codestyle_src
code_test: codestyle_test
code: codestyle
codestyle_src:
	${PYCODESTYLE_BASE} ${SRC}
codestyle_test:
	 ${PYCODESTYLE_BASE} ${TEST}

# PyDocStyle Only
PYDOCSTYLE_BASE=${PYTHON} -m pydocstyle
docstyle: docstyle_src docstyle_test
doc_src: docstyle_src
doc_test: docstyle_test
docs: docstyle
docstyle_src:
	${PYDOCSTYLE_BASE} ${SRC}
docstyle_test:
	${PYDOCSTYLE_BASE} ${TEST}
codetest:
	${CODE_TEST}
codeall: code codetest
doc: docstyle
doc:
	${DOC_SRC}

# Testing
test:
	${PYTHON} -m unittest discover -v
testdoc:
	${PYTHON} -m test.test --doctests-only
test_all: test testdoc
test_survey_cto: #TODO: run a single unit test
	${PYTHON} -m unittest discover -v
DEMO_IN=test/files/multiple_file_language_option_conversion
DEMO_OUT=~/Desktop/ppp-demo
demo:
	mkdir ${DEMO_OUT}
	for file in ${DEMO_IN}/*.xlsx; do \
		cp $$file ${DEMO_OUT}; \
	done
	python3 -m ppp ${DEMO_OUT}/*.xlsx -f doc html -p minimal full -l English Français


# Package Management
build:
	rm -rf ./dist && rm -rf ./build && ${PYTHON} setup.py sdist bdist_wheel
dist: build
pypi_push_test:
	make build && twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pypi_push:
	make build && twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
pypi_test: pypi_push_test
pip_test: pypi_push_test
pypi: pypi_push
pip: pypi_push

# Scripts
paper:
	sh ./scripts/generic_paper_questionnaires.sh
