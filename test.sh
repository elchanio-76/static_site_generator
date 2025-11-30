#!/bin/bash

# This script is used to run the unit tests for the project.
# Activate the virtual environment.
source .venv/bin/activate

# Run the unit tests.
python -m unittest discover -s src
