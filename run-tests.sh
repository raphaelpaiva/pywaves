#!/bin/bash

TEST_PATTERN="*_test.py"
INIT_PATTERN="*__init__*"

PYTHON_PATH=$1
PYTHON=${PYTHON_PATH}python
rm -f .coverage

$PYTHON -m coverage run --omit=$TEST_PATTERN,$INIT_PATTERN -a -m unittest discover -p *_test.py
$PYTHON -m coverage html
