#!/bin/sh

# Create a virtual environment
python3 -m venv venv

# Activate the virtualenv
. venv/bin/activate

# install the dependencies
pip install -r requirements.txt

# run the script
python3 main.py
