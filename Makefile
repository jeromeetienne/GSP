##########################################################################
# Makefile for GSP project


##########################################################################
# Test targets

test:
	cd tests
	pytest

test_verbose:
	cd tests
	pytest -v

##########################################################################

examples_output_force_commit:
	git add -f examples/output
	git commit -m "Force commit of recent examples/output images"

##########################################################################
# Download examples data 

download_examples_data: download_lidar_data

download_lidar_data:
	# Download the lidar data from the specified URL
	# The URL points to a specific commit in the data repository
	# The file is saved as lidar.npz in the current directory
	# The ?download= at the end of the URL is used to ensure it downloads correctly
	curl -L https://github.com/datoviz/data/raw/4edb8c26e0145c9180b28f7469680d09dca3bbf3/misc/lidar.npz\?download\= > ./examples/data/lidar.npz

##########################################################################
# Documentation targets
#

build_doc:
	# Build the documentation using MkDocs
	mkdocs build

open_doc: build_doc
	# Open the documentation in the default web browser
	open site/index.html

serve_doc:
	# Serve the documentation locally - useful for development - open in browser with http://localhost:8000
	mkdocs serve