#!/bin/env python
# -*- coding: utf-8 -*-

import operator
from project.solvers.base_solution import BaseSolution
from project import models

class ClarkeWrightSolution(BaseSolution):
    """Class for a Clarke and Wright Savings algorithm"""

    def __init__(self, cvrp_problem, vehicles):
        """Initialize class

        Parameters:
            cvrp_problem: CVRPData instance
            vehicles: Vehicles number
        """
        self._routes = [models.Route(cvrp_problem.capacity()) for _ in range(vehicles)]
        self._problem = cvrp_problem
        self._nodes = {x.name(): models.Node(x.name(), x.demand()) for x in cvrp_problem.nodes()}
        self._allocated = 0

    def get_pair(self, pair):
        i, j = pair
        return (self._nodes[i], self._nodes[j])

    def clone(self):
        """Returns a deep copy of self

        Clones:
            routes
            allocation
            nodes
        """

        new_solution = ClarkeWrightSolution(self._problem, len(self._routes))

        # Clone routes
        for index, r in enumerate(self._routes):
            new_route = new_solution._routes[index]
            for node in r.nodes():
                # Insere new node on new route
                new_node = new_solution._nodes[node]
                new_route.allocate([new_node])

        return new_solution

    def process(self, pair):
        """Processes a pair of nodes into the current solution

        MUST CREATE A NEW INSTANCE, NOT CHANGE ANY INSTANCE ATTRIBUTES

        Returns a new instance (deep copy) of self object
        """
        a, b = pair

        new_solution = self.clone()

        i, j = new_solution.get_pair((a, b))

        if i.route_allocation() is None and j.route_allocation() is None:
            # Try to add the two nodes to a route
            for route in new_solution._routes:
                if route.can_allocate([i, j]):
                    route.allocate([i, j])
                    new_solution._allocated = new_solution._allocated + 2
                    break
        # either i or j is allocated
        elif ((i.route_allocation() is not None and j.route_allocation() is None) or
                (j.route_allocation() is not None and i.route_allocation() is None)):
            inserted = None
            to_insert = None

            if i.route_allocation() is not None:
                inserted = i
                to_insert = j
            else:
                inserted = j
                to_insert = i

            route = inserted.route_allocation()

            # inserted not interior
            if not route.is_interior(inserted):
                if route.can_allocate([to_insert]):
                    append = False

                    if route.last(inserted):
                        append = True

                    route.allocate([to_insert], append)
                    new_solution._allocated = new_solution._allocated + 1

        return new_solution

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

    def routes(self):
        """Returns a generator for iterating over solution routes"""
        for r in self._routes:
            yield r

    def length(self):
        """Returns the solution length (or cost)"""
        length = 0
        for r in self._routes:
            length = length + self._problem.length(r)

        return length

def compute_savings_list(data):
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

def simulation(solution, savings_list):
    """Do a Monte Carlo Simulation"""
    pass

def solve(data, vehicles):
    """Solves the CVRP problem using Clarke and Wright Savings methods"""
    savings_list = compute_savings_list(data)

    solution = ClarkeWrightSolution(data, vehicles)

    for i, j in savings_list:
        if solution.can_process((i, j)):
            solution = solution.process((i, j))

    return list(solution.routes()), savings_list
