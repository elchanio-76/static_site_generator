#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run the application
python3 src/main.py
cd public && python3 -m http.server 8888