#!/bin/env python
# -*- coding: utf-8 -*-

import sys

from project import data_input, util
from project.solvers import clarke_wright, binary_mcscws

def usage():
    print "python {} <tspblib_file> <vehicles_number>".format(sys.argv[0])

def main():
    if len(sys.argv) != 3: # python main.py <file> <vehicles_number>
        return usage()

    clarke_wright_solver = clarke_wright.ClarkeWrightSolver()
    binary_mcscws_solver = binary_mcscws.BinaryMCSCWSSolver()

    data = data_input.read_file(sys.argv[1])
    vehicles = int(sys.argv[2])

    routes, savings_list = clarke_wright_solver.solve(data, vehicles)

    print 'SAVINGS LIST MATRIX'
    print savings_list

    util.print_solution(routes)

if __name__ == '__main__':
    main()
