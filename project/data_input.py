#!/bin/env python
# -*- coding: utf-8 -*-

import re
import math

from os import path

class ParseException(Exception):
    """Exception raised when something unexpected occurs in a TSPLIB file parsing"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def strip(line):
    """Removes any \r or \n from line and remove trailing whitespaces"""
    return line.replace('\r\n', '').strip() # remove new lines and trailing whitespaces

def sanitize(filename):
    """Returns a sanitized file name with absolut path

    Example: ~/input.txt -> /home/<your_home/input.txt
    """
    return path.abspath(path.expanduser(path.expandvars(filename)))

def _parse_depot_section(f):
    """Parse TSPLIB DEPOT_SECTION data part from file descriptor f

    Returns an array of depots
    """
    depots = []

    for line in f:
        line = strip(line)
        if line == '-1': # End of section
            break
        else:
            depots.append(line)

    return depots

def _parse_nodes_section(f, current_section, nodes):
    """Parse TSPLIB NODE_COORD_SECTION or DEMAND_SECTION from file descript f

    Returns a dict containing the node as key
    """
    section = {}
    dimensions = None

    if current_section == 'NODE_COORD_SECTION':
        dimensions = 3 # i: (i, j)
    elif current_section == 'DEMAND_SECTION':
        dimensions = 2 # i: q
    else:
        raise ParseException('Invalid section {}'.format(current_section))

    n = 0
    for line in f:
        line = strip(line)

        # Check dimensions
        definitions = re.split('\s*', line)
        if len(definitions) != dimensions:
            raise ParseException('Invalid dimensions from section {}. Expected: {}'.format(current_section, dimensions))

        node = int(definitions[0])
        values = [int(v) for v in definitions[1:]]

        section[node] = values

        n = n + 1
        if n == nodes:
            break

    # Assert all nodes were read
    if n != nodes:
        raise ParseException('Missing {} nodes definition from section {}'.format(nodes - n, current_section))

    return section

def calculate_euc_distance(a, b):
    """Calculates Eclidian distances from two points a and b

    Points are two-dimension tuples
    """
    x1, y1 = a
    x2, y2 = b

    return math.sqrt(((x1 - x2) ** 2) + (((y1 - y2) ** 2)))


def _post_process_specs(specs):
    """Post-process specs after pure parsing

    Casts any number expected values into integers

    Remarks: Modifies the specs object
    """
    integer_specs = ['DIMENSION', 'CAPACITY']

    for s in integer_specs:
        specs[s] = int(specs[s])

def _create_node_matrix(specs):
    """Calculates distances between nodes and model it in a upper triangular matrix

    'MATRIX' key added to `specs`
    """
    distances = specs['NODE_COORD_SECTION']
    dimensions = specs['DIMENSION']

    specs['MATRIX'] = {}

    for i in distances:
        origin = tuple(distances[i])

        specs['MATRIX'][i] = {}

        for j in specs['NODE_COORD_SECTION']:
            destination = tuple(distances[j])

            distance = calculate_euc_distance(origin, destination)

            #
            # Upper triangular matrix
            # if i > j, ij = 0
            #
            if i > j:
                continue

            specs['MATRIX'][i][j] = distance

def _setup_depot(specs):
    """Setup depot model

    'DEPOT' key added to `specs`
    """
    specs['DEPOT'] = specs['DEPOT_SECTION']

def _post_process_data(specs):
    """Post-process specs data after complete parsing

    Processes:
        - Calculates distances and model it in a matrix
        - Setup depot model
    """

    _create_node_matrix(specs)
    _setup_depot(specs)

def _parse_tsplib(f):
    """Parses a TSPLIB file descriptor and returns a dict containing the problem definition"""
    line = ''

    specs = {}

    used_specs = ['NAME', 'COMMENT', 'DIMENSION', 'CAPACITY', 'TYPE']
    used_data = ['NODE_COORD_SECTION', 'DEMAND_SECTION', 'DEPOT_SECTION']

    # Parse specs part
    for line in f:
        line = strip(line)

        # Arbitrary sort, so we test everything out
        for s in used_specs:
            if line.startswith(s):
                specs[s] = line.split('{} :'.format(s))[-1].strip() # get value data part
                break

        # All specs read
        if len(specs) == len(used_specs):
            break

    if len(specs) != len(used_specs):
        raise ParseException('Error parsing TSPLIB data: specs {} missing'.format(set(used_specs) - set(specs)))

    _post_process_specs(specs)

    # Parse data part
    for line in f:
        line = strip(line)

        for d in used_data:
            if line.startswith(d):
                if d == 'DEPOT_SECTION':
                    specs[d] = _parse_depot_section(f)
                else:
                    specs[d] = _parse_nodes_section(f, d, specs['DIMENSION'])

        if len(specs) == len(used_specs) + len(used_data):
            break

    if len(specs) != len(used_specs) + len(used_data):
        missing_specs = set(specs) - (set(used_specs) + set(used_data))
        raise ParseException('Error parsing TSPLIB data: specs {} missing'.format(missing_specs))

    _post_process_data(specs)

    return specs

def read_file(filename):
    """Reads a TSPLIB file and returns the problem data"""
    sanitized_filename = sanitize(filename)

    f = open(sanitized_filename)

    specs = None

    try:
        specs = _parse_tsplib(f)
    except ParseException:
        raise
    finally: # 'finally' is executed even when we re-raise exceptions
        f.close()

    if specs['TYPE'] != 'CVRP':
        raise Exception('Not a CVRP TSPLIB problem. Found: {}'.format(specs['TYPE']))
