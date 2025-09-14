help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/:.*##/:/' | column -t -s:

##############################################################################

lint_checker: lint_checker_src lint_checker_examples ## Run pyright type checker on src and examples

lint_checker_src: ## Run pyright type checker on ./src
	pyright src/**/*.py

lint_checker_examples: ## Run pyright type checker on ./examples
	pyright examples/**/*.py

##############################################################################

run_all_examples: ## Run all examples to check they run without error
	python examples/run_all_examples.py