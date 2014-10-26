#!/bin/env python
# -*- coding: utf-8 -*-

from project.solvers import base

class CentroideSolution(base.BaseSolution):
    """Base abstract class for Centroide-based CVRP solution"""

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
        raise NotImplementedError()