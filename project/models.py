#!/bin/env python
# -*- coding: utf-8 -*-

class Route(object):
    """Class for modelling a CVRP route"""

    def __init__(self, cvrp_problem, capacity):
        """Class constructor

        Initialize route capacity

        Parameters:
            capacity: route capacity
        """
        self._problem = cvrp_problem
        self._capacity = capacity
        self._demand = 0
        self._nodes = []

    def capacity(self):
        """Returns the route capacity"""
        return self._capacity

    def demand(self):
        """Returns the current route demand"""
        return self._demand

    def nodes(self):
        """Returns a generator for iterating over nodes"""
        for node in self._nodes:
            yield node

    def length(self):
        """Returns the route length (cost)"""
        cost = 0
        depot = self._problem.depot()

        last = depot
        for i in self._nodes:
            a, b = last, i
            if a > b:
                a, b = b, a

            cost = cost + self._problem.distance(a, b)
            last = i

        cost = cost + self._problem.distance(depot, last)

        return cost

    def can_allocate(self, nodes):
        """Returns True if this route can allocate nodes in `nodes` list"""
        nodes_demand = sum([node.demand() for node in nodes])

        if self._demand + nodes_demand <= self._capacity:
            return True

        return False

    def allocate(self, nodes, append=True):
        """Allocates all nodes from `nodes` list in this route"""
        if not self.can_allocate(nodes):
            raise Exception('Trying to allocate more than route capacity')

        nodes_demand = 0
        for node in [node for node in nodes]:
            if node._allocation:
                node._allocation.deallocate([node])

            node._allocation = self
            nodes_demand = nodes_demand + node.demand()
            if append:
                self._nodes.append(node)
            else:
                self._nodes.insert(0, node)

        self._demand = self._demand + nodes_demand

    def deallocate(self, nodes):
        """Deallocates all nodes from `nodes` list from this route"""
        nodes_demand = 0
        for node in nodes:
            self._nodes.remove(node)
            node._allocation = None
            nodes_demand = nodes_demand + node.demand()

        self._demand = self._demand - nodes_demand

        if self._demand < 0:
            raise Exception('Trying to deallocate more than previously allocated')

    def is_interior(self, node):
        """Returns True if node is interior to the route, i.e., not adjascent to depot"""
        return self._nodes.index(node) != 0 and self._nodes.index(node) != len(self._nodes) - 1

    def last(self, node):
        """Returns True if node is the last node in the route"""
        return self._nodes.index(node) == len(self._nodes) - 1

    def __str__(self):
        return str(self._nodes)

    def __repr__(self):
        return str(self._nodes)

class Node(object):
    """Class for modelling a CVRP node"""

    def __init__(self, name, demand):
        """Class constructor

        Initialize demand

        Parameters:
            name: Node name
            demand: Node demand
        """
        self._name = name
        self._demand = demand
        self._allocation = None

    def name(self):
        """Returns node name"""
        return self._name

    def demand(self):
        """Returns the node demand"""
        return self._demand

    def route_allocation(self):
        """Returns the route which node is allocated"""
        return self._allocation

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)

    def __cmp__(self, other):
        if isinstance(other, Node):
            return self._name - other._name

        return self._name - other

    def __hash__(self):
        return self._name.__hash__()

class CVRPData(object):
    """Class for modelling a CVRP problem data"""

    def __init__(self, data):
        """Class constructor

        Initialize all nodes, edges and depot

        Parameters:
            data: TSPLIB parsed data
        """
        self._nodes = {i: Node(i, data['DEMAND'][i]) for i in data['MATRIX']}
        self._matrix = {}
        self._capacity = data['CAPACITY']
        self._depot = None

        for i in data['MATRIX']:

            x = self._nodes[i]
            self._matrix[x] = {}

            if i == data['DEPOT']:
                self._depot = x # x, not i!!

            for j in data['MATRIX']:
                if i > j:
                    continue

                y = self._nodes[j]

                self._matrix[x][y] = data['MATRIX'][i][j]

        if self._depot is None:
            raise Exception('Depot not found')

    def nodes(self):
        """Returns a generator for iterating over nodes"""
        for i in sorted(self._nodes):
            yield self._nodes[i]

    def edges(self):
        """Returns a generator for iterating over edges"""
        for i in sorted(self._matrix.keys()):
            for j in sorted(self._matrix[i].keys()):
                if i != j:
                    yield (i, j)

    def depot(self):
        """Returns the depot node"""
        return self._depot

    def distance(self, i, j):
        """Returns the distance between node i and node j"""
        a, b = i, j

        if a.name > b.name:
            a, b = b, a

        return self._matrix[a][b]

    def capacity(self):
        """Returns vehicles capacity"""
        return self._capacity
