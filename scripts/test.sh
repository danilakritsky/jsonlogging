#!/usr/bin/env bash

set -e
set -x

coverage run -m unittest discover tests
coverage report