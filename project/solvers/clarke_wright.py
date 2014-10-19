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

        print 'i', i
        print 'old_vehicle', old_vehicle
        print 'vehicles_demand', vehicles_demand

        if old_vehicle < len(vehicles_demand):
            vehicles_demand[old_vehicle] = vehicles_demand[old_vehicle] - demand
        else:
            print 'como nao?'

        print 'vehicles_demand depois', vehicles_demand

        if i in vehicles_run[old_vehicle]:
            print 'ta aqui'
            vehicles_run[old_vehicle].remove(i)
        else:
            print '{} not in vehicles_run'.format(old_vehicle)

        # # Remove 0-nodes routes
        # if not vehicles_run[old_vehicle]:
        #     del vehicles_demand[old_vehicle]
        #     del vehicles_run[old_vehicle]

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

    sorted_savings_list = sorted(savings_list.items(), key=operator.itemgetter(1))

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

    # for i, j in savings_list:
    #     #
    #     # (I)   t(0,i) and t(0, j) must be greater than zero.
    #     # (II)  p(i) and p(y) are not already allocated on the same truck run.
    #     # (III) Removing the trucks allocated to Q(i) and Q(j) and adding a truck to cover the load Q(i)+Q(j)
    #     #       does not cause the trucks allocated to exceed the trucks available
    #     #
    #     if routes[depot][i] > 0 and routes[depot][j] > 0:
    #         if allocations[i] != allocations[j]:
    #             vehicle_a = allocations[i]
    #             vehicle_b = allocations[j]

    #             if can_add(data, j, vehicles_demand[vehicle_a]):
    #                 add_node(data, allocations, j, vehicle_a, vehicles_run, vehicles_demand)
    #                 routes[i][j] = 1
    #                 routes[depot][i] = 1
    #                 routes[depot][j] = 1
    #             elif can_add(data, i, vehicles_demand[vehicle_b]):
    #                 add_node(data, allocations, i, vehicle_b, vehicles_run, vehicles_demand)
    #                 routes[i][j] = 1
    #                 routes[depot][i] = 1
    #                 routes[depot][j] = 1

    vehicles_run = [[] for _ in range(vehicles)]
    vehicles_demand = [0 for _ in range(vehicles)]
    allocations = {}

    print 'savings length', len(savings_list)

    while savings_list:
        break
        for i, j in savings_list:

            exausted = False

            print vehicles_run
            print 'iterating {}'.format((i, j))

            demand = data['DEMAND'][i] + data['DEMAND'][j]

            # Neither points are in a route
            if i not in allocations and j not in allocations:
                # Try to add to a route
                fodeu_count = 0
                for vehicle in range(vehicles):
                    if can_add(data, i, vehicles_demand[vehicle]) and can_add(data, j, vehicles_demand[vehicle]):
                        add_node(data, allocations, i, vehicle, vehicles_run, vehicles_demand)
                        add_node(data, allocations, j, vehicle, vehicles_run, vehicles_demand)
                        exausted = True
                        break
                    else:
                        fodeu_count = fodeu_count + 1
                        print 'fodeu'

                if fodeu_count == vehicles:
                    print len(savings_list)
                    print vehicles_demand
                    raise Exception('fodeu')
            elif i in allocations and j not in allocations or i in allocations and j not in allocations: # either i or j is allocated
                print '{} or {} not allocated'.format(i, j)

                inserted = None
                to_insert = None

                if i in allocations:
                    inserted = i
                    to_insert = j
                else:
                    inserted = j
                    to_insert = i

                if vehicles_run[allocations[inserted]].index(inserted) == 0 or vehicles_run[allocations[inserted]].index(inserted) == len(vehicles_run[allocations[inserted]]) - 1: # i not interior
                    print '{} is not interior'.format(inserted)
                    if can_add(data, to_insert, vehicles_demand[allocations[inserted]]):

                        append = False

                        if vehicles_run[allocations[inserted]].index(inserted) == len(vehicles_run[allocations[inserted]]) - 1:
                            append = True

                        add_node(data, allocations, to_insert, allocations[inserted], vehicles_run, vehicles_demand, append)

                    exausted = True
            elif i in allocations and j in allocations and allocations[i] != allocations[j]: # both allocated
                both_not_interior = vehicles_run[allocations[i]].index(i) == 0 or vehicles_run[allocations[i]].index(i) == len(vehicles_run[allocations[i]]) - 1
                both_interior = not both_not_interior

                both_not_interior = both_not_interior and (vehicles_run[allocations[j]].index(j) == 0 or vehicles_run[allocations[j]].index(j) == len(vehicles_run[allocations[j]]) - 1)
                both_interior = both_interior and (vehicles_run[allocations[j]].index(j) != 0 and vehicles_run[allocations[j]].index(j) != len(vehicles_run[allocations[j]]) - 1)

                print 'both_not_interior? {}'.format(both_not_interior)

                if both_not_interior:
                    # Merge routes
                    if can_add(data, j, vehicles_demand[allocations[i]]):
                        append = False

                        if vehicles_run[allocations[i]].index(i) == len(vehicles_run[allocations[i]]) - 1:
                            append = True

                        add_node(data, allocations, j, allocations[i], vehicles_run, vehicles_demand, append)
                        exausted = True
                        print 'merged'
                    elif can_add(data, i, vehicles_demand[allocations[j]]):
                        append = False

                        if vehicles_run[allocations[j]].index(j) == len(vehicles_run[allocations[j]]) - 1:
                            append = True

                        add_node(data, allocations, i, allocations[j], vehicles_run, vehicles_demand, append)
                        exausted = True
                        print 'merged'
                    exausted = True

                if both_interior:
                    exausted = True
                    print 'both interior'


            if exausted:
                print 'exausted'
                savings_list.remove((i, j))
                break

    print 'vehicles_run', vehicles_run

    return routes, savings_list, vehicles_run