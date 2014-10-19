#!/bin/env python
# -*- coding: utf-8 -*-

import operator

def can_add(data, i, current):
    """Returns true if a vehicle with demand `current` has capacity to serve `i`"""
    demand = data['DEMAND'][i]
    capacity = data['CAPACITY']

    if current + demand <= capacity:
        return True

    return False

def add_node(data, allocation, i, vehicle, vehicles_run, vehicles_demand):
    """Adds node `i` to vehicle `vehicle`

    Takes care of removing demand for one vehicle to another
    """
    demand = data['DEMAND'][i]

    #
    # Removes demand from old vehicle
    #
    if i in allocation:
        old_vehicle = allocation[i]

        vehicles_demand[old_vehicle] = vehicles_demand[old_vehicle] - demand
        vehicles_run[old_vehicle].remove(i)

        # Remove 0-nodes routes
        if not vehicles_run[old_vehicle]:
            del vehicles_demand[old_vehicle]
            del vehicles_run[old_vehicle]

    vehicles_demand[vehicle] = vehicles_demand[vehicle] + demand
    vehicles_run[vehicle].append(i)
    allocation[i] = vehicle

    return True


def create_initial_routes(data, vehicles_run, vehicles_demand):
    """Creates a list of initial routes

    First, a route contains only two nodes: the depot and a node

    Returns a tuple contaning the routing table and an allocation matrix (node -> vehicle)
    """
    routes = {}
    allocation = {}

    depot = data['DEPOT']

    for i in data['MATRIX']:
        routes[i] = {}

        for j in data['MATRIX'][i]:
            if i > j:
                continue

            if i == j:
                continue

            if i == depot:
                vehicles_demand[j] = 0
                vehicles_run[j] = []

                add_node(data, allocation, j, j, vehicles_run, vehicles_demand)

                routes[i][j] = 2
            else:
                routes[i][j] = 0

    return routes, allocation


def compute_savings_list(data):
    """Compute Clarke and Wright savings list

    A saving list is a matrix containing the saving amount S between i and j

    S is calculated by S = d(0,i) + d(0,j) - d(i,j) (CLARKE; WRIGHT, 1964)
    """

    depot = data['DEPOT']

    savings_list = {}

    for i in data['MATRIX']:
        if i == depot:
            continue

        for j in data['MATRIX']:
            if j == depot:
                continue

            if i > j: # upper triangular matrix
                continue

            if i == j:
                continue

            t = (i, j)

            savings_list[t] = data['MATRIX'][depot][i] + data['MATRIX'][depot][j] - data['MATRIX'][i][j]

    sorted_savings_list = sorted(savings_list.items(), key=operator.itemgetter(1), reverse=True)

    return [nodes for nodes, saving in sorted_savings_list]

def solve(data, vehicles):
    """Solves the CVRP problem using Clarke and Wright Savings methods"""
    savings_list = compute_savings_list(data)

    vehicles_run = {}
    vehicles_demand = {}

    initial_routes, allocations = create_initial_routes(data, vehicles_run, vehicles_demand)
    routes = initial_routes.copy()

    print vehicles_run
    print vehicles_demand

    depot = data['DEPOT']

    for i, j in savings_list:
        #
        # (I)   t(0,i) and t(0, j) must be greater than zero.
        # (II)  p(i) and p(y) are not already allocated on the same truck run.
        # (III) Removing the trucks allocated to Q(i) and Q(j) and adding a truck to cover the load Q(i)+Q(j)
        #       does not cause the trucks allocated to exceed the trucks available
        #
        if routes[depot][i] > 0 and routes[depot][j] > 0:
            if allocations[i] != allocations[j]:
                vehicle_a = allocations[i]
                vehicle_b = allocations[j]

                if can_add(data, j, vehicles_demand[vehicle_a]):
                    add_node(data, allocations, j, vehicle_a, vehicles_run, vehicles_demand)
                    routes[i][j] = 1
                    routes[depot][i] = 1
                    routes[depot][j] = 1
                elif can_add(data, i, vehicles_demand[vehicle_b]):
                    add_node(data, allocations, i, vehicle_b, vehicles_run, vehicles_demand)
                    routes[i][j] = 1
                    routes[depot][i] = 1
                    routes[depot][j] = 1

    print 'vehicles_run', vehicles_run

    return routes, savings_list, [j for i, j in vehicles_run.items()]
