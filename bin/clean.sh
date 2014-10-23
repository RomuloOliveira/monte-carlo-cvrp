#!/bin/bash

# Uncomment to delete all previous tests
# find -name '*.out' -path './out/*' -print0 | xargs --no-run-if-empty -0 rm -v

find -name '*.pyc' -print0 | xargs --no-run-if-empty -0 rm -v
