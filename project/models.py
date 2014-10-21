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
        raise NotImplementedError()

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
