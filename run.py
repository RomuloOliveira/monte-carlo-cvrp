#!/bin/env python
# -*- coding: utf-8 -*-

import sys

from project import data_input

def usage():
    print "python {} <tspblib_file> <vehicles_number>".format(sys.argv[0])

def main():
    if len(sys.argv) != 3: # python main.py <file> <vehicles_number>
        return usage()

    data, vehicles = data_input.read_file(sys.argv[1]), sys.argv[2]
    data, vehicles

if __name__ == '__main__':
    main()
