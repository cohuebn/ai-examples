# Overview

This repository is meant to show how to use various AI tools ([OpenAI](https://openai.com/), [LangChain](https://python.langchain.com/docs/get_started/introduction.html), etc.) to integrate AI into custom applications. It is broken down into various examples used to illustrate different common use-cases for AI within custom applications.

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
5. You also should setup your .env file with any relevant API keys (e.g. OpenAI key).

## Running an example Python module

Some modules are Python only (no other infrastructure required). These can be run directly via
Python commands if desired. To run them take these steps:

1. If it isn't already, ensure you've activated your venv within the terminal session: `. .venv/bin/activate`
2. Run the example module. This corresponds to the directory in the examples folder: `python -m examples/<folder_name>`

## Running an example requiring additional infrastructure

Some modules require additional infrastructure along with Python scripts. The additional infrastructure is created in Docker. To run, take these steps:

1. Start up the Docker containers: `./infrastructure/local.start.sh`
2. [Run the Python example](#running-an-example-python-module)
3. Stop the Docker containers: `./infrastructure/local.stop.sh`
