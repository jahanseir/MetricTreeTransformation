from covertree import CoverTree
from point import Point
from node import Node
from greedypermutation import GreedyPermutation
from CHeap import CHeap
from CPoint import CPoint
from timeit import default_timer
from metrics import *
import random

def main():
#     points = [Point([i*10, j*10]) for i in range(20) for j in range(20)]
#     points = [Point([random.randint(-1000000, 1000000) for dim in range(2)]) for num in range(600)]
    f = open('btc2mil.txt', 'r')
    f.readline()
    f.readline()
    points = []
    for i in range(2000):
        elem = f.readline().split()
        points.append(Point([float(elem[0]), float(elem[1]), float(elem[2])]))
    metric = Euclidean()
    start = default_timer()
    perm = CHeap([CPoint(p.pt) for p in points], metric).makePerm()
    print('Greedy permutation using CHeap with {0} distance computation: {1:.2f} s'.format(metric.counter, default_timer() - start))
    metric.counter = 0
    start = default_timer()
    perm = GreedyPermutation(points, metric).makePerm()
    print('Greedy permutation with {0} distance computation: {1:.2f} s'.format(metric.counter, default_timer() - start))
    metric.counter = 0
    ct = CoverTree(metric, 2)
    start = default_timer()
    ct.buildFromGP(perm)
    print('Build cover tree from greedy permutation with {0} distance computation: {1:.2f} s'.format(metric.counter, default_timer() - start))
    ct.report()
    random.shuffle(points)
    metric.counter = 0
    ct3 = CoverTree(metric, 2)
    start = default_timer()
    for p in points:
        ct3.dynamicInsert2(p)
    print('Build cover tree dynamically with depth first search with {0} distance computation: {1:.2f} s'.format(metric.counter, default_timer() - start))
    ct3.report()
    print('finished.')
    
if __name__ == "__main__":
    main()
