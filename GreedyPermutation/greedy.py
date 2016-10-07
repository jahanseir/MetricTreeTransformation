#!/usr/bin/env python

from sys import stdin
from greedyheap import GreedyHeap
from point import Point

if __name__ == '__main__':
    h = GreedyHeap()
    for line in stdin:
        coords = [float(x) for x in line.split()]
        h.insert(Point(coords))

    while not h.isempty():
        print(h.removeMax())
