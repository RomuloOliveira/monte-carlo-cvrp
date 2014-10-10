#!/bin/bash

flake8 --exclude='build/*,venv/*' --max-line-length=120 --ignore=E302,F403,E261 .
