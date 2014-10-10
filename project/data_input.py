#!/bin/env python
# -*- coding: utf-8 -*-

import os

def sanitize(filename):
    """Returns a sanitized file name with absolut path

    Example: ~/input.txt -> /home/<your_home/input.txt
    """
    # TODO: Sanitize
    # See #1
    return filename

def read_file(filename):
    """Reads a TSPLIB file and returns the problem data"""
    sanitized_filename = sanitize(filename)

    line = ''

    specs = {}

    used_specs = ['NAME', 'COMMENT', 'DIMENSION', 'CAPACITY', 'TYPE']
    used_data = ['NODE_COORD_SECTION', 'DEMAND_SECTION', 'DEPOT_SECTION']

    # Parse specs part
    for line in open(sanitized_filename):
        line = line.replace('\r\n', '').strip() # remove new lines and trailing whitespaces
        for s in used_specs:
            if line.startswith(s):
                print s, line
                specs[s] = line.split('{} :'.format(s))[-1].strip() # get value data part
                break

        # All specs read
        if len(specs) == len(used_specs):
            break

    if len(specs) != len(used_specs):
        raise Exception('Error parsing TSPLIB data: {} missing'.format(set(used_specs) - set(specs)))

    print specs