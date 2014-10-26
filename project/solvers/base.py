#!/bin/env python
# -*- coding: utf-8 -*-

from project import models

class BaseSolution(object):
    """Base abstract class for a CVRP solution"""

    def __init__(self, cvrp_problem, vehicles):
        """Initialize class

        Parameters:
            cvrp_problem: CVRPData instance
            vehicles: Vehicles number
        """
        self._routes = [models.Route(cvrp_problem, cvrp_problem.capacity()) for _ in range(vehicles)]
        self._problem = cvrp_problem
        self._nodes = {x.name(): models.Node(x.name(), x.demand()) for x in cvrp_problem.nodes()}
        self._allocated = 0

    def get_pair(self, pair):
        i, j = pair
        return (self._nodes[i], self._nodes[j])

    def is_complete(self):
        """Returns True if this is a complete solution, i.e, all nodes are allocated"""
        return all(
            [node.route_allocation() is not None for node in self._nodes.values() if node != self._problem.depot()]
        )

    def clone(self):
        """Returns a deep copy of self

        Clones:
            routes
            allocation
            nodes
        """

        new_solution = self.__class__(self._problem, len(self._routes))

        # Clone routes
        for index, r in enumerate(self._routes):
            new_route = new_solution._routes[index]
            for node in r.nodes():
                # Insere new node on new route
                new_node = new_solution._nodes[node]
                new_route.allocate([new_node])

        return new_solution

    def routes(self):
        """Returns a generator for iterating over solution routes"""
        for r in self._routes:
            yield r

    def length(self):
        """Returns the solution length (or cost)"""
        length = 0
        for r in self._routes:
            length = length + r.length()

        return length

    def can_process(self, pairs):
        """Returns True if this solution can process `pairs`

        Parameters:
            pairs: List of pairs
        """
        raise NotImplementedError()

    def process(self, node_or_pair):
        """Processes a node or a pair of nodes into the current solution

        MUST CREATE A NEW INSTANCE, NOT CHANGE ANY INSTANCE ATTRIBUTES

        Returns a new instance (deep copy) of self object
        """
        raise NotImplementedError()


class BaseSolver(object):
    """Base algorithm solver class"""

    def solve(self, data, vehicles, timeout):
        """Must solves the CVRP problem

        Parameters:
            data: CVRPData instance
            vehicles: Vehicles number
            timeout: max processing time in seconds

        Must return BEFORE timeout

        Must returns a solution (BaseSolution class derived)
        """
        raise NotImplementedError()
