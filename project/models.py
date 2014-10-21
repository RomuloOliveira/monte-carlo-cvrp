#!/bin/env python
# -*- coding: utf-8 -*-

class Vehicle(object):
    """Class for modelling a CVRP vehicle"""

    def __init__(self, capacity):
        """Class constructor

        Initialize vehicle capacity

        Parameters:
            capacity: vehicle capacity
        """
        self._capacity = capacity
        self._demand = 0

    def capacity(self):
        """Returns the vehicle capacity"""
        return self._capacity

    def demand(self):
        """Returns the current vehicle demand"""
        return self._demand

    def can_allocate(self, nodes):
        """Returns True if this vehicle can allocate nodes in `nodes` list"""
        nodes_demand = sum([node.demand() for node in nodes])

        if self._demand + nodes_demand <= self._capacity:
            return True

        return False

    def allocate(self, nodes):
        """Allocates all nodes from `nodes` list in this vehicle"""
        if self.can_allocate(nodes) == False:
            raise Exception('Trying to allocate more than vehicle capacity')

        nodes_demand = sum([node.demand() for node in nodes])

        self._demand = self._demand + nodes_demand

    def deallocate(self, nodes):
        """Deallocates all nodes from `nodes` list from this vehicle"""
        nodes_demand = sum([node.demand() for node in nodes])

        self._demand = self._demand - nodes_demand

        if self._demand < 0:
            raise Exception('Trying to deallocate more than previously allocated')

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

    def vehicle_allocation(self):
        """Returns the vehicle which node is allocated"""
        return self._allocation

    def allocate(self, vehicle):
        """Allocates the current node into `vehicle`"""
        if self._allocation:
            self._allocation.deallocate(self)

        vehicle.allocate(self)
        self._allocation = vehicle

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)

class CVRPData(object):
    """Class for modelling a CVRP problem data"""

    def __init__(self, data):
        """Class constructor

        Initialize all nodes, edges and vehicles

        Parameters:
            data: TSPLIB parsed data
        """
        self._matrix = {}
        self._capacity = data['CAPACITY']

        for i in data['MATRIX']:

            x = Node(i, data['DEMAND'][i])
            self._matrix[x] = {}

            for j in data['MATRIX']:
                if i > j:
                    continue

                y = Node(j, data['DEMAND'][j])

                self._matrix[x][y] = data['MATRIX'][i][j]

    def nodes(self):
        """Returns a generator for iterating over nodes"""
        for i in sorted(self._matrix):
            yield i

    def edges(self):
        """Returns a generator for iterating over edges"""
        for i in sorted(self._matrix.keys()):
            for j in sorted(self._matrix[i]):
                yield (i, j)

    def distance(self, i, j):
        """Returns the distance between node i and node j"""
        return self._matrix[i][j]

    def capacity(self):
        """Returns vehicles capacity"""
        return self._capacity
