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

    routes, savings_list, vehicles_run = clarke_wright.solve(data, vehicles)

    print 'DISTANCE MATRIX'
    util.print_upper_triangular_matrix(data['MATRIX'])

    print 'SAVINGS LIST MATRIX'
    print savings_list

    print 'ROUTING MATRIX'
    util.print_upper_triangular_matrix(routes)

    print 'SOLUTIONS'
    total_cost = 0
    for solution in vehicles_run:
        cost = util.solution_length(data, solution)
        total_cost = total_cost + cost
        print '{}: {}'.format(solution, cost)
    print 'Total cost: {}'.format(total_cost)

    optimum = [
        [25, 28],
        [27, 8, 14, 18, 20, 32, 22],
        [7, 4, 3, 24, 29, 5, 12, 15],
        [31, 17, 2, 13],
        [30, 19, 9, 10, 23, 16, 11, 26, 6, 21]
    ]

    print 'OPTIMAL SOLUTIONS'
    total_cost = 0
    for solution in optimum:
        cost = util.solution_length(data, solution)
        total_cost = total_cost + cost
        print '{}: {}'.format(solution, cost)
    print 'Total cost: {}'.format(total_cost)

if __name__ == '__main__':
    main()
