#!/bin/env python
# -*- coding: utf-8 -*-

import operator
import time

import random

from project import models

from project.solvers.base import BaseSolver
from project.solvers.clarke_wright import ClarkeWrightSolution

class MonteCarloSavingsSolution(ClarkeWrightSolution):
    """Solution class for a Clarke and Wright Savings algorithm using Monte Carlo Savings algorithm (OLIVEIRA, 2014)"""

    def __init__(self, cvrp_problem, vehicles):
        super(MonteCarloSavingsSolution, self).__init__(cvrp_problem, vehicles)

        self._vehicles = vehicles
        self._routes = [models.Route(cvrp_problem, cvrp_problem.capacity()) for _ in range(len(self._nodes) - 1)]

        for i, node in enumerate([node for node in self._nodes.values() if node != cvrp_problem.depot()]):
            self._routes[i].allocate([node])

    def clone(self):
        """Returns a deep copy of self

        Clones:
            routes
            allocation
            nodes
        """

        new_solution = self.__class__(self._problem, self._vehicles)

        # Clone routes
        for index, r in enumerate(self._routes):
            new_route = new_solution._routes[index] = models.Route(self._problem, self._problem.capacity())
            for node in r.nodes():
                # Insere new node on new route
                new_node = new_solution._nodes[node]
                new_route.allocate([new_node])

        return new_solution

    def is_complete(self):
        """Returns True if this is a complete solution, i.e, all nodes are allocated"""
        allocated = all(
            [node.route_allocation() is not None for node in self._nodes.values() if node != self._problem.depot()]
        )

        valid_routes = len(self._routes) == self._vehicles

        valid_demands = all([route.demand() <= route.capacity() for route in self._routes])

        return allocated and valid_routes and valid_demands

class MonteCarloSavingsSolver(BaseSolver):
    """Clark and Wright Savings algorithm solver class"""

    default_lambda_p = 0.05

    def __init__(self, lambda_p=None, *args, **kwargs):
        super(MonteCarloSavingsSolver, self).__init__()

        if lambda_p is None:
            lambda_p = self.default_lambda_p

        self._lambda_p = lambda_p

    def compute_list_of_savings_list(self, data):
        """Compute Clarke and Wright savings list

        A saving list is a matrix containing the saving amount S between i and j

        S is calculated by S = d(0,i) + d(0,j) - d(i,j) + P

        Returns a list of savings list, ordered by total saving
        """

        for r in range(2000):
            savings_list = {}

            total_savings = 0

            for i, j in data.edges():
                t = (i, j)

                if i == data.depot() or j == data.depot():
                    continue

                p = random.uniform(-self._lambda_p, self._lambda_p)

                saving = data.distance(data.depot(), i) + data.distance(data.depot(), j) - data.distance(i, j)
                saving = saving + (saving * p)

                total_savings = total_savings + saving

                savings_list[t] = saving

            sorted_savings_list = sorted(savings_list.items(), key=operator.itemgetter(1), reverse=True)

            yield [nodes for nodes, saving_count in sorted_savings_list]

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using Monte Carlo Savings method (OLIVEIRA, 2014)

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (MonteCarloSavingsSolution class))
        """
        start = time.time()
        time_found = None

        best = MonteCarloSavingsSolution(data, vehicles)
        best_feasible = best

        savings_lists = self.compute_list_of_savings_list(data)

        solution_lengths = 0
        processed_count = 0

        for savings_list in savings_lists:
            solution = MonteCarloSavingsSolution(data, vehicles)

            for i, j in savings_list[:]:
                if solution.is_complete():
                    break

                if solution.can_process((i, j)):
                    solution, inserted = solution.process((i, j))

                if time.time() - start > timeout:
                    break

            if time.time() - start > timeout:
                break

            if solution.is_complete() and not best_feasible.is_complete():
                best_feasible = solution
            elif solution.is_complete() and solution.length() < best.length():
                best_feasible = solution

            if solution.length() < best.length():
                best = solution
                time_found = time.time() - start

            processed_count = processed_count + 1
            solution_lengths = solution_lengths + solution.length()

        print 'best solution found on {}'.format(time_found)

        if processed_count:
            print 'average solution lengths: {}'.format(solution_lengths / float(processed_count))

        if not best.is_complete():
            from project import util
            print 'Best solution not feasible, printing best feasible found'
            util.print_solution(best_feasible)

        return best
