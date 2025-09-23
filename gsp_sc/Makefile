help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/:.*##/:/' | column -t -s:

##############################################################################

lint: lint_src lint_examples ## Run pyright type checker on src and examples

lint_src: ## Run pyright type checker on ./src
	pyright src/

lint_examples: ## Run pyright type checker on ./examples
	pyright examples/

##############################################################################

run_all_examples: ## Run all examples to check they run without error
	python scripts/run_all_examples.py

check_expected_output: ## Check that the output files match the expected output files
	python scripts/check_expected_output.py

test: lint run_all_examples check_expected_output ## Run all tests
	@echo "All tests passed!"