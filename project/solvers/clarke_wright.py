#!/bin/env python
# -*- coding: utf-8 -*-

import operator

def can_add(data, i, remaining_demand):
    """Returns true if a vehicle with remaining demand `remaining_demand` has capacity to serve `i`"""
    demand = data['DEMAND'][i]

    if remaining_demand - demand >= 0:
        return True

    return False

def add_node(data, allocation, i, vehicle, vehicles_run, vehicles_remaining_demand):
    """Adds node `i` to vehicle `vehicle`

    Takes care of removing demand for one vehicle to another
    """
    demand = data['DEMAND'][i]

    #
    # Removes demand from old vehicle
    #

    if i in allocation:
        old_vehicle = allocation[i]

        if old_vehicle:
            vehicles_remaining_demand[old_vehicle] = vehicles_remaining_demand[old_vehicle] + demand
            vehicles_run[old_vehicle].remove(i)

    vehicles_remaining_demand[vehicle] = vehicles_remaining_demand[vehicle] - demand
    vehicles_run[vehicle].append(i)
    allocation[i] = vehicle

    return True


def create_initial_routes(data, vehicles_run, vehicles_remaining_demand):
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

            if i == depot:
                added = False

                for vehicle_index in range(len(vehicles_run)):
                    if can_add(data, j, vehicles_remaining_demand[vehicle_index]):
                        added = add_node(data, allocation, j, vehicle_index, vehicles_run, vehicles_remaining_demand)
                        break

                if added:
                    routes[i][j] = 2
                else:
                    raise Exception('Could not allocate node {}'.format(j))

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
    vehicles_remaining_demand = [data['CAPACITY'] for _ in range(vehicles)]

    initial_routes, allocations = create_initial_routes(data, vehicles_run, vehicles_remaining_demand)
    routes = initial_routes.copy()

    # print vehicles_run
    # print vehicles_remaining_demand

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
                    vehicle_a_remaind_demand = vehicles_remaining_demand[vehicle_a]

                    vehicle_b = allocations[j]
                    vehicle_b_remaind_demand = vehicles_remaining_demand[vehicle_b]

                    if can_add(data, j, vehicle_a_remaind_demand):
                        add_node(data, allocations, j, vehicle_a, vehicles_run, vehicles_remaining_demand)
                        routes[i][j] = 1
                        routes[depot][i] = 1
                        routes[depot][j] = 1
                    elif can_add(data, i, vehicle_b_remaind_demand):
                        add_node(data, allocations, i, vehicle_b, vehicles_run, vehicles_remaining_demand)
                        routes[i][j] = 1
                        routes[depot][i] = 1
                        routes[depot][j] = 1

    print 'vehicles_run', vehicles_run

    return routes, savings_list, vehicles_run
