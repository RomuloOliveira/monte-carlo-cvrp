#!/bin/env python
# -*- coding: utf-8 -*-

import sys

from project import data_input

def usage():
    print "python {} <tspblib_file>".format(sys.argv[0])

def main():
    if len(sys.argv) != 2: # python main.py <file>
        return usage()

    data = data_input.read_file(sys.argv[1])
    data

if __name__ == '__main__':
    main()
