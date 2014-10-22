#!/bin/env python
# -*- coding: utf-8 -*-

import random

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
            if solution.can_process((i, j)):
                if random.random() > 0.2:
                    solution = solution.process((i, j))

        if solution.is_complete() and (solution.length() < self._best.length() or not self._best.is_complete()):
            self._best = solution

        return solution.length()

    def solve(self, data, vehicles):
        """Solves the CVRP problem using BinaryMCS-CWS method

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number

        Returns a solution (BinaryMCSCWSSolution class))
        """
        savings_list = self.compute_savings_list(data)

        solution = BinaryMCSCWSSolution(data, vehicles)
        self._best = solution

        for i, j in savings_list:
            if solution.can_process((i, j)):
                processed = solution.process((i, j))

                yes = 0
                no = 0

                for r in range(50): # simulations
                    yes = yes + self.simulation(processed, (i, j), savings_list[:])
                    no = no + self.simulation(solution, (i, j), savings_list[:])

                if yes < no:
                    solution = processed

            if solution.is_complete() and (solution.length() < self._best.length() or not self._best.is_complete()):
                self._best = solution

        return self._best
