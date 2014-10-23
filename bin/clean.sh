#!/bin/bash

find -name '*.pyc' -print0 | xargs --no-run-if-empty -0 rm -v
