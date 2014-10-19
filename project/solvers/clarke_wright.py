#!/bin/env python
# -*- coding: utf-8 -*-

import operator

def can_add(data, node_list, current):
    """Returns true if a vehicle with demand `current` has capacity to serve `node_list`"""
    demand = sum([data['DEMAND'][i] for i in node_list])
    capacity = data['CAPACITY']

    if current + demand <= capacity:
        return True

    return False

def add_node(data, allocation, i, vehicle, vehicles_run, vehicles_demand, append=True):
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

    vehicles_demand[vehicle] = vehicles_demand[vehicle] + demand
    allocation[i] = vehicle

    if append: # append
        vehicles_run[vehicle].append(i)
    else: # prepend
        vehicles_run[vehicle].insert(0, i)

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
                if j % 5 not in vehicles_demand:
                    vehicles_demand[j % 5] = 0

                if j % 5 not in vehicles_run:
                    vehicles_run[j % 5] = []

                add_node(data, allocation, j, j % 5, vehicles_run, vehicles_demand)

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

    vehicles_run = [[] for _ in range(vehicles)]
    vehicles_demand = [0 for _ in range(vehicles)]
    allocations = {}
    dimension = data['DIMENSION']

    for i, j in savings_list:

        if len(allocations) == dimension - 1:
            break

        demand = data['DEMAND'][i] + data['DEMAND'][j]

        # Neither points are in a route
        if i not in allocations and j not in allocations:
            # Try to add the two nodes to a route
            for vehicle in range(vehicles):
                if can_add(data, [i, j], vehicles_demand[vehicle]):
                    add_node(data, allocations, i, vehicle, vehicles_run, vehicles_demand)
                    add_node(data, allocations, j, vehicle, vehicles_run, vehicles_demand)
        elif (i in allocations and j not in allocations) or (j in allocations and i not in allocations): # either i or j is allocated
            inserted = None
            to_insert = None

            if i in allocations:
                inserted = i
                to_insert = j
            else:
                inserted = j
                to_insert = i

            if vehicles_run[allocations[inserted]].index(inserted) == 0 or vehicles_run[allocations[inserted]].index(inserted) == len(vehicles_run[allocations[inserted]]) - 1: # i not interior
                if can_add(data, [to_insert], vehicles_demand[allocations[inserted]]):
                    append = False

                    if vehicles_run[allocations[inserted]].index(inserted) == len(vehicles_run[allocations[inserted]]) - 1:
                        append = True

                    add_node(data, allocations, to_insert, allocations[inserted], vehicles_run, vehicles_demand, append)

    return vehicles_run, savings_list
