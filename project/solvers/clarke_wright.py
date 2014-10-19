#!/bin/env python
# -*- coding: utf-8 -*-

def create_initial_routes(data):
    """Creates a list of initial routes

    First, a route contains only two nodes: the depot and a node
    """
    routes = []

    depot = data['DEPOT']

    for i in data['MATRIX']:

        current_route = [depot]

        if i != depot:
            current_route.append(i)

            routes.append(current_route)

    return routes


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

        savings_list[i] = {}

        for j in data['MATRIX']:
            if j == depot:
                continue

            if i > j: # upper triangular matrix
                continue

            if i == j:
                continue

            savings_list[i][j] = data['MATRIX'][depot][i] + data['MATRIX'][depot][j] - data['MATRIX'][i][j]

    return savings_list

def solve(data, vehicles):
    """Solves the CVRP problem using Clarke and Wright Savings methods"""

    initial_routes = create_initial_routes(data)

    routes = initial_routes[:]

    savings_list = compute_savings_list(data)

    # for edge in savings_list:
    #     new_route, old_route = try_merge(edge)

    #     if new_route:
    #         routes.remove(old_route)

    return routes, savings_list
