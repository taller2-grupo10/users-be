#!/bin/sh
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
exec "$@"