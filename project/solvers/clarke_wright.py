#!/bin/env python
# -*- coding: utf-8 -*-

import operator
import time

from project import models

from project.solvers.base import BaseSolution, BaseSolver

class ClarkeWrightSolution(BaseSolution):
    """Solution class for a Clarke and Wright Savings parallel algorithm"""

    def __init__(self, cvrp_problem, vehicles):
        super(ClarkeWrightSolution, self).__init__(cvrp_problem, vehicles)

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

    def process(self, pair):
        """Processes a pair of nodes into the current solution

        MUST CREATE A NEW INSTANCE, NOT CHANGE ANY INSTANCE ATTRIBUTES

        Returns a new instance (deep copy) of self object
        """
        a, b = pair

        new_solution = self.clone()

        i, j = new_solution.get_pair((a, b))

        route_i = i.route_allocation()
        route_j = j.route_allocation()

        inserted = False

        if ((route_i is not None and route_j is not None) and (route_i != route_j)):
            if route_i._nodes.index(i) == 0 and route_j._nodes.index(j) == len(route_j._nodes) - 1:
                if route_j.can_allocate(route_i._nodes):
                    route_j.allocate(route_i._nodes)

                    if i.route_allocation() != j.route_allocation():
                        raise Exception('wtf')

                    inserted = True
            elif route_j._nodes.index(j) == 0 and route_i._nodes.index(i) == len(route_i._nodes) - 1:
                if route_i.can_allocate(route_j._nodes):
                    route_i.allocate(route_j._nodes)

                    if i.route_allocation() != j.route_allocation():
                        raise Exception('wtf j')

                    inserted = True

        new_solution._routes = [route for route in new_solution._routes if route._nodes]

        return new_solution, inserted

    def can_process(self, pairs):
        """Returns True if this solution can process `pairs`

        Parameters:
            pairs: List of pairs
        """
        i, j = pairs

        # Neither points are in a route
        if i.route_allocation() is None or j.route_allocation() is None:
            return True

        if self._allocated == len(list(self._problem.nodes())) - 1: # All nodes in a route
            return False

        return False

class ClarkeWrightSolver(BaseSolver):
    """Clark and Wright Savings algorithm solver class"""
    def compute_savings_list(self, data):
        """Compute Clarke and Wright savings list

        A saving list is a matrix containing the saving amount S between i and j

        S is calculated by S = d(0,i) + d(0,j) - d(i,j) (CLARKE; WRIGHT, 1964)
        """

        savings_list = {}

        for i, j in data.edges():
            t = (i, j)

            if i == data.depot() or j == data.depot():
                continue

            savings_list[t] = data.distance(data.depot(), i) + data.distance(data.depot(), j) - data.distance(i, j)

        sorted_savings_list = sorted(savings_list.items(), key=operator.itemgetter(1), reverse=True)

        return [nodes for nodes, saving in sorted_savings_list]

    def solve(self, data, vehicles, timeout):
        """Solves the CVRP problem using Clarke and Wright Savings methods

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Returns a solution (ClarkeWrightSolution class))
        """
        savings_list = self.compute_savings_list(data)

        solution = ClarkeWrightSolution(data, vehicles)

        start = time.time()

        for i, j in savings_list[:]:
            if solution.is_complete():
                break

            if solution.can_process((i, j)):
                solution, inserted = solution.process((i, j))

                if inserted:
                    savings_list.remove((i, j))

            if time.time() - start > timeout:
                break

        return solution
