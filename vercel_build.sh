#!/usr/bin/env python3
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/pip install setuptools
.venv/bin/pip install build
.venv/bin/python3 -m build