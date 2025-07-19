
# Graphic Server Protocol (GSP)

The Graphic Server Protocol (GSP) defines the protocol used between a visualization library or a visualization software a language server that provides graphical features.

# Installation
## How to install repository for development

Create a virtual environment:

```bash
python3 -m venv gcp_env
source gcp_env/bin/activate
```

Then install the packages:

```bash
pip install .
```

## How to run tests

Install pytest package
```bash
pip install pytest
```

how to run tests
```
cd tests
pytest
```

how to run tests in verbose mode
```
cd tests
pytest -v
```

## How to launch examples

From the root of the repository, navigate to the examples directory:
```bash
cd ./examples
```

To List all examples
```
ls -l *.py
```

To launch one example
```
python ./points-3d.py
```

## How to use Makefile

Run the test
```
make test
```

Run the tests in verbose mode
```
make test-verbose
```

## How to generate documentation

Install the mkdocs-material package

```
pip install mkdocs-material
pip install "markdown-exec[ansi]"
```

Generate the documentation in the ```./site``` directory
```
mkdocs build  
```

## How to download the examples data

Download the data from https://github.com/datoviz/data/tree/main

```
make download_examples_data
```

