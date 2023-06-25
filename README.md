# Prerequisites

- Python 3 is installed on your machine. Recommendation: use [pyenv](https://github.com/pyenv/pyenv) to manage your Python installation.
  - [Brew install pyenv on mac](https://github.com/pyenv/pyenv#homebrew-in-macos)

# Building and running locally

## Installing dependencies

This section describes how to install all required dependencies for this application. While the virtual environment is optional, it helps keep dependencies isolated from other Python projects on your machine.

1. Create a new virtual environment in this directory: `python -m venv --copies .venv`.

   - Note the `--copies` flag
     which is important to get VS Code intellisense working correctly as it doesn't work as well when the Python interpreter is a symlink. Symlink'ing is the default way the interpreter is setup when using the `venv` module

2. Activate that virtual environment: `. .venv/bin/activate`
3. Ensure the build tools are installed and up-to-date: `pip install --upgrade build pip`
4. Install dependencies: `pip install .`. If you also want dev dependencies (linting, dotenv loading, etc.) also run `python -m pip install '.[dev]'`

## Running the main script

1. If it isn't already, ensure you've activated your venv within the terminal session: `. .venv/bin/activate`
2. Run the main entrypoint: `python .`
