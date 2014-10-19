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
    util.print_upper_triangular_matrix(savings_list)

    print 'ROUTING MATRIX'
    util.print_upper_triangular_matrix(routes)

    print 'VEHICLES RUN'
    print vehicles_run


if __name__ == '__main__':
    main()
