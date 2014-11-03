#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

from project.solvers import base

class CentroideSolution(base.BaseSolution):
    """Base abstract class for Centroide-based CVRP solution"""

    def _get_farthest_not_allocated_node(self, node):
        """Returns the farthest node from `node`

        Does not returns the depot
        """
        depot = self._problem.depot()

        far_far_away_node = None
        far_far_away_distance = -1

        for current_node in self._nodes.values():
            if current_node != depot and current_node != node and current_node.route_allocation() is None:
                if far_far_away_node is None:
                    far_far_away_node = current_node
                    far_far_away_distance = self._problem.distance(node, current_node)
                else:
                    distance = self._problem.distance(node, current_node)
                    if distance > far_far_away_distance:
                        far_far_away_node = current_node
                        far_far_away_distance = distance

        return far_far_away_node

    def _get_nearest_not_allocated_node(self, node):
        """Returns the nearest node from `node`

        Does not returns the depot
        """
        depot = self._problem.depot()

        nearest_node = None
        nearest_distance = sys.maxsize

        for current_node in self._nodes.values():
            if current_node != depot and current_node != node and current_node.route_allocation() is None:
                if nearest_node is None:
                    nearest_node = current_node
                    nearest_distance = self._problem.distance(node, current_node)
                else:
                    distance = self._problem.distance(node, current_node)
                    if distance < nearest_distance:
                        nearest_node = current_node
                        nearest_distance = distance

        return nearest_node

    def generate_clusters(self):
        """Generates `vehicles` clusters containing next nodes"""

        new_solution = self.clone()

        while not new_solution.is_complete():
            for r in new_solution._routes:
                # new_solution._get_nearest_not_allocated_node(depot)
                far_far_away_node = random.choice(new_solution._nodes.values())

                if far_far_away_node is None:
                    break

                if random.random() > 0.2:
                    break

                if r.can_allocate([far_far_away_node]):
                    r.allocate([far_far_away_node])
                    new_solution._allocated = new_solution._allocated + 1

                for i in range(len(new_solution._nodes)):
                    node = new_solution._get_nearest_not_allocated_node(far_far_away_node)

                    if random.random() > 0.2:
                        break

                    if node and node.route_allocation() is None:
                        if r.can_allocate([node]):
                            r.allocate([node])
                            new_solution._allocated = new_solution._allocated + 1

        return new_solution

class CentroideSolver(base.BaseSolver):
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

        base_solution = CentroideSolution(data, vehicles)
        best = base_solution

        for r in range(1000):
            solution = base_solution.generate_clusters()

            print list(solution.routes())

            if solution.is_complete() and (not best.is_complete() or solution.length() < best.length()):
                best = solution

        return best
