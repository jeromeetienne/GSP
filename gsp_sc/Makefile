##############################################################################

lint_checker: lint_checker_src lint_checker_examples

lint_checker_src:
	pyright src/**/*.py

lint_checker_examples:
	pyright examples/**/*.py

##############################################################################

test_examples:
	python examples/test_all.py