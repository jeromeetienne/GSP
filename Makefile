test:
	cd tests
	pytest

test_verbose:
	cd tests
	pytest -v

examples_output_force_commit:
	git add -f examples/output
	git commit -m "Force commit of recent examples/output images"