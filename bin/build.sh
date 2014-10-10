#!/bin/bash

set -e

find -name '*.pyc' -print0 | xargs --no-run-if-empty -0 rm

pip install --upgrade -r requirements.txt

. bin/lint.sh
