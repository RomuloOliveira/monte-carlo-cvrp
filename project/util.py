#!/bin/env python
# -*- coding: utf-8 -*-

def print_upper_triangular_matrix(matrix):
    """Prints a CVRP data dict matrix"""

    # Print column header
    # Assumes first row contains all needed headers
    first = sorted(matrix.keys())[0]
    print '\t',
    for i in matrix[first]:
        print '{}\t'.format(i),
    print

    indent_count = 0

    for i in matrix:
        # Print line header
        print '{}\t'.format(i),

        if indent_count:
            print '\t' * indent_count,

        for j in sorted(matrix[i]): # required because dict doesn't guarantee insertion order
            print '{}\t'.format(matrix[i][j]),

        print

        indent_count = indent_count + 1
