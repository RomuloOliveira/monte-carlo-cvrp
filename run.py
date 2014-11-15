#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from project import data_input, util
from project.solvers import clarke_wright, sequential_clarke_wright, mcs_clarke_wright, binary_mcscws # , centroide

def usage():
    print "python {} <tspblib_file> <vehicles_number> [<lambda_p>]".format(sys.argv[0])

def main():
    if len(sys.argv) < 3: # python main.py <file> <vehicles_number> [<p>]
        return usage()

    data = data_input.read_file(sys.argv[1])
    vehicles = int(sys.argv[2])

    lambda_p = None

    if sys.argv == 4:
        lambda_p = float(sys.argv[3])

    clarke_wright_solver = clarke_wright.ClarkeWrightSolver()
    sequential_clarke_wright_solver = sequential_clarke_wright.SequentialClarkeWrightSolver()
    mcs_clarke_wright_solver = mcs_clarke_wright.MCSClarkeWrightSolver(lambda_p)
    binary_mcscws_solver = binary_mcscws.BinaryMCSCWSSolver()
    # centroide_solver = centroide.CentroideSolver()
    # parallel_binary_mcscws_solver = parallel_binary_mcscws.ParallelBinaryMCSCWSSolver()

    timeout = 300

    algorithms = [
        (clarke_wright_solver, 'ClarkeWrightSolver'),
        (sequential_clarke_wright_solver, 'SequentialClarkeWrightSolver'),
        (mcs_clarke_wright_solver, 'MCSClarkeWrightSolver'),
        # (binary_mcscws_solver, 'BinaryMCSCWSSolver'),
        # (centroide_solver, 'CentroideSolver')
    ]

    best_algorithm = None
    best_solution = None

    for solver, algorithm in algorithms:
        start = time.time()

        solution = solver.solve(data, vehicles, timeout)

        elapsed = time.time() - start

        if not solution.is_complete():
            print 'Solution from algorithm {} not a complete solution'.format(algorithm)

        print '{} solution:'.format(algorithm)
        util.print_solution(solution)

        print 'Elapsed time (seconds): {}'.format(elapsed)

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
