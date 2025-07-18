
# Graphic Server Protocol (GSP)

The Graphic Server Protocol (GSP) defines the protocol used between a visualization library or a visualization software a language server that provides graphical features.

# Installation
## How to install repository

Create a virtual environment and install the package:

```bash
python3 -m venv gcp_env
source gcp_env/bin/activate
```

Then install the package:

```bash
pip install -e .
```

## How to run tests

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