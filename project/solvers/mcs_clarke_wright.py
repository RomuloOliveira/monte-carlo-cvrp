#!/bin/env python
# -*- coding: utf-8 -*-

import operator
import time

import random

from project import models

from project.solvers.base import BaseSolver
from project.solvers.sequential_clarke_wright import SequentialClarkeWrightSolution

class MCSClarkeWrightSolution(SequentialClarkeWrightSolution):
    """Solution class for a Clarke and Wright Savings algorithm using Monte Carlo Methods"""

    def __init__(self, cvrp_problem, vehicles):
        super(MCSClarkeWrightSolution, self).__init__(cvrp_problem, vehicles)

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

class MCSClarkeWrightSolver(BaseSolver):
    """Clark and Wright Savings algorithm solver class"""

    def compute_list_of_savings_list(self, data):
        """Compute Clarke and Wright savings list

        A saving list is a matrix containing the saving amount S between i and j

        S is calculated by S = d(0,i) + d(0,j) - d(i,j) + P

        Returns a list of savings list, ordered by total saving
        """

        multiple_savings_lists = []

        p = 0.05

        for r in range(2000):
            savings_list = {}

            total_savings = 0

            for i, j in data.edges():
                t = (i, j)

                if i == data.depot() or j == data.depot():
                    continue

                if random.random() > 0.5:
                    p = -p

                saving = data.distance(data.depot(), i) + data.distance(data.depot(), j) - data.distance(i, j)
                saving = saving + (p * saving)

                total_savings = total_savings + saving

                savings_list[t] = saving

            sorted_savings_list = sorted(savings_list.items(), key=operator.itemgetter(1), reverse=True)

            yield [nodes for nodes, saving in sorted_savings_list]

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using Clarke and Wright Savings methods

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (MCSClarkeWrightSolution class))
        """
        start = time.time()
        time_found = None

        best = MCSClarkeWrightSolution(data, vehicles)

        savings_lists = self.compute_list_of_savings_list(data)

        for savings_list in savings_lists:
            solution = MCSClarkeWrightSolution(data, vehicles)

            for i, j in savings_list[:]:
                if solution.is_complete():
                    break

                if solution.can_process((i, j)):
                    solution, inserted = solution.process((i, j))

                if time.time() - start > timeout:
                    break

            if time.time() - start > timeout:
                break

            if solution.is_complete() and not best.is_complete():
                best = solution
                time_found = time.time() - start
            elif solution.is_complete() and solution.length() < best.length():
                best = solution
                time_found = time.time() - start

        print 'best solution found on {}'.format(time_found)

        return best
