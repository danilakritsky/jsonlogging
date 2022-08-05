#!/usr/bin/env bash

set -x
set -e

mypy jsonlogging
black jsonlogging tests
isort jsonlogging tests
flake8 jsonlogging tests
