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

def print_upper_triangular_matrix_as_complete(matrix):
    """Prints a CVRP data dict upper triangular matrix as a normal matrix

    Doesn't print header"""
    count = sorted(matrix.keys())[0]

    for i in sorted(matrix.keys()):
        for j in sorted(matrix.keys()):
            a, b = i, j
            if a > b:
                a, b = b, a

            print matrix[a][b],

        print

def solution_length(data, solution):
    """Returns the solution length cost

    Solution is a list of node indexes
    """

    cost = 0
    depot = data['DEPOT']

    last = depot
    for i in solution:
        a, b = last, i
        if a > b:
            a, b = b, a

        cost = cost + data['MATRIX'][a][b]
        last = i

    cost = cost + data['MATRIX'][depot][last]

    return cost
