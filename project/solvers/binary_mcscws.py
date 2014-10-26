#!/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from project.solvers import clarke_wright

class BinaryMCSCWSSolution(clarke_wright.ClarkeWrightSolution):
    """Solution class for a BinaryMCS-CWS algorithm"""

class BinaryMCSCWSSolver(clarke_wright.ClarkeWrightSolver):
    """BinaryMCS-CWS algorithm solver class"""

    def __init__(self):
        self._best = None

    def simulation(self, solution, pair, savings_list):
        """Do a Monte Carlo Simulation"""
        for i, j in savings_list:
            if solution.is_complete():
                break

            if solution.can_process((i, j)):
                if random.random() > 0.15:
                    solution, inserted = solution.process((i, j))

        if self._best is None:
            self._best = solution
        elif solution.is_complete() and (solution.length() < self._best.length()):
            self._best = solution

        return solution.length(), solution.is_complete()

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using BinaryMCS-CWS method

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (BinaryMCSCWSSolution class))
        """
        start = time.time()
        savings_list = self.compute_savings_list(data)

        solution = BinaryMCSCWSSolution(data, vehicles)
        self._best = None

        savings_copy = savings_list[:]

        while savings_list:
            i, j = savings_list.pop(0)

            if solution.is_complete():
                break

            if solution.can_process((i, j)):
                processed, inserted = solution.process((i, j))

                if not inserted:
                    continue

                minimum_yes = 9999999
                minimum_no = 9999999

                for r in range(50): # simulations
                    length, complete = self.simulation(processed.clone(), (i, j), savings_copy)

                    if complete:
                        if length < minimum_yes:
                            minimum_yes = length


                    length, complete = self.simulation(solution.clone(), (i, j), savings_copy)

                    if complete:
                        if length < minimum_no:
                            minimum_no = length

                    if time.time() - start > timeout:
                        break

                print 'minimum_yes', minimum_yes
                print 'minimum_no', minimum_no

                if minimum_yes <= minimum_no:
                    print 'yes'
                    solution = processed
                else:
                    print 'no'

                print self._best.length()

                print

            if time.time() - start > timeout:
                break

        print 'Constructed solution {}. Complete? {}'.format(solution.length(), solution.is_complete())

        if self._best is None:
            self._best = solution
        elif solution.is_complete() and (solution.length() < self._best.length()):
            self._best = solution

        return self._best
