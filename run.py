#!/bin/env python
# -*- coding: utf-8 -*-

import sys

from project import data_input, util
from project.solvers import clarke_wright

def usage():
    print "python {} <tspblib_file> <vehicles_number>".format(sys.argv[0])

def main():
    if len(sys.argv) != 3: # python main.py <file> <vehicles_number>
        return usage()

    data = data_input.read_file(sys.argv[1])
    vehicles = int(sys.argv[2])

    routes, savings_list = clarke_wright.solve(data, vehicles)

    # print 'DISTANCE MATRIX'
    # util.print_upper_triangular_matrix(data['MATRIX'])

    # print 'COMPLETE MATRIX'
    # util.print_upper_triangular_matrix_as_complete(data['MATRIX'])

    print 'SAVINGS LIST MATRIX'
    print savings_list

    print 'SOLUTIONS'
    total_cost = 0
    for solution in routes:
        cost = data.length(solution)
        total_cost = total_cost + cost
        print '{}: {}'.format(solution, cost)
    print 'Total cost: {}'.format(total_cost)

if __name__ == '__main__':
    main()
