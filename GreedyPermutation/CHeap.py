from heapq import heapify, heappush
from point import Point
import math

class CHeap:
    def __init__(self, points, metric):
        self.points = []  # input points
        for p in points:
            if p in self.points: print('point {} is already in the permutation'.format(p))
            else:
                p.metric = metric
                p.pred = None
                p.dis = float('inf')
                self.points.append(p)
        self.metric = metric
        self.heap = []  # a max heap for centers of clusters, key is max dist of a center to its cluster
        self.perm = []  # generated permutation
        self.eps = float('inf')
        
    def makePerm(self):
        # Init heap
        point = self.points.pop(0)        
        for pt in self.points:
            point.addRNN(pt)
        point.setCenterDist()             
        self.perm.append(Point(point.pt, float('inf'), None))
        heappush(self.heap, point)
        while len(self.points) != 0:
            # find farthest point from its center
            top = self.heap[0]
            farthest = top.rnnPop()
            self.points.remove(farthest)
            farthest.updatePred(top)
            top.setCenterDist()
            # create a new cluster
            for nbr in farthest.pred.neighbors:
                farthest.newCenter(nbr)
                if nbr.rnnIsEmpty() and nbr in self.heap:
                    heapchanged = True
                    self.heap.remove(nbr)
            heapify(self.heap)
            # find the right neighbors
            for p in self.heap:
                if p.dist(self.metric, farthest)[0] < 4 * farthest.dis:
                    p.neighbors.append(farthest)
                    farthest.neighbors.append(p)
            # add farthest point to the permutation and heapify its cluster
            pred = [p for p in self.perm if p.pt == farthest.pred.pt][0]
            self.perm.append(Point(farthest.pt, farthest.dist(self.metric, pred)[0], pred))
            if not farthest.rnnIsEmpty():
                farthest.setCenterDist()
                heappush(self.heap, farthest)
            
#             if len(self.heap) == 0:continue 
#             prevcenter = farthest
#             rk = self.heap[0].rnnPeek().dis
#             while prevcenter.pred is not None and prevcenter.pred.radius <= 4 * rk:
#                 prevcenter = prevcenter.pred           
#             if farthest.dist(self.metric, prevcenter)[0] > 4 * rk:
#                 print('no')            
#             i = 0;
#             while i < len(prevcenter.neighbors):
#                 p = prevcenter.neighbors[i]
#                 if p.dist(self.metric, prevcenter)[0] > 8 * rk:
#                     prevcenter.neighbors.remove(p)
#                     i -= 1
#                 elif p.dist(self.metric, farthest)[0] < 4 * rk:
#                     p.neighbors.append(farthest)
#                     farthest.neighbors.append(p)
#                 i += 1
        return self.perm