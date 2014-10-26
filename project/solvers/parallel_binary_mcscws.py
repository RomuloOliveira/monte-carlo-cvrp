#!/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from multiprocessing import Pool, Lock, Manager

from project.solvers import binary_mcscws

class ParallelBinaryMCSCWSSolution(binary_mcscws.BinaryMCSCWSSolution):
    """Solution class for parallel BinaryMCS-CWS algorithm"""
    pass

lock = Lock()
namespace = Manager().Namespace()
namespace.best = None

def simulation((solution, pair, savings_list)):
    """Do a Monte Carlo Simulation

    it's NOT a class method
    """
    global namespace
    global lock

    for i, j in savings_list:
        if solution.can_process((i, j)):
            if random.random() > 0.4:
                solution = solution.process((i, j))

    with lock:
        if solution.is_complete() and (solution.length() < namespace.best.length() or not namespace.best.is_complete()):
            namespace.best = solution

    if solution.is_complete():
        return solution.length()

    return solution.length() + 1000

class ParallelBinaryMCSCWSSolver(binary_mcscws.BinaryMCSCWSSolver):
    """A parallel BinaryMCS-CWS algorithm solver class"""

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using BinaryMCS-CWS method

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (ParallelBinaryMCSCWSSolution class))
        """
        global namespace
        global lock

        start = time.time()
        savings_list = self.compute_savings_list(data)

        solution = ParallelBinaryMCSCWSSolution(data, vehicles)
        namespace.best = solution

        p = Pool(10)

        for i, j in savings_list:
            if solution.is_complete():
                break

            if solution.can_process((i, j)):
                processed = solution.process((i, j))

                yes = 0
                no = 0

                async_y = p.map_async(simulation, [(processed, (i, j), savings_list[:]) for r in range(20)])
                async_n = p.map_async(simulation, [(solution, (i, j), savings_list[:]) for r in range(20)])

                yes = async_y.get()
                no = async_n.get()

                if yes < no:
                    solution = processed

            with lock:
                if (solution.is_complete() and
                        (solution.length() < namespace.best.length() or not namespace.best.is_complete())):
                    namespace.best = solution

            if time.time() - start > timeout:
                break

        p.close()
        p.join()

        return namespace.best
