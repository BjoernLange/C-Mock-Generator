#!/bin/bash
flake8 --count --show-source --statistics
mypy .
pylint **/*.py --disable=C0114 --disable=C0115 --disable=C0116 --exit-zero
