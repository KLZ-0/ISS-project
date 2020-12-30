#!/bin/sh

# Create a virtual environment
python3 -m venv venv || exit 1

# Activate the virtualenv
. venv/bin/activate || exit 1

# install the dependencies
pip install -r requirements.txt || exit 1

# run the script
python3 main.py
