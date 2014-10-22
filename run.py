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

    cws_solution = clarke_wright_solver.solve(data, vehicles)
    binary_mcscws_solution = binary_mcscws_solver.solve(data, vehicles)

    solutions = [(cws_solution, 'ClarkeWrightSolver'), (binary_mcscws_solution, 'BinaryMCSCWSSolver')]
    valid_solutions = []

    for solution, algorithm in solutions:
        if not solution.is_complete():
            print 'Solution from algorithm {} not a complete solution'.format(algorithm)
        else:
            print '{} solution:'.format(algorithm)
            util.print_solution(solution)

            valid_solutions.append((solution, algorithm))

    best_solution = None
    best_algorithm = None

    for solution, algorithm in solutions:
        if best_algorithm is None:
            best_algorithm = algorithm

        if best_solution is None:
            best_solution = solution

        if solution.length() < best_solution.length():
            best_solution = solution
            best_algorithm = algorithm

    print
    print 'Best: {}'.format(best_algorithm)

if __name__ == '__main__':
    main()
