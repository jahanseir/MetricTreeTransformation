import math
from heapq import heapify, heappush, heappop
import point

class GreedyHeap:
    def __init__(self):
        self.heap = []  # points in the heap
        self.pts = []   # points already removed (used to compute keys)
        
    def insert(self, pt):
        # compute key
        for p in self.pts:
            pt.updatepred(p)
        
        heappush(self.heap, pt)

    def removeMax(self):
        p = heappop(self.heap)
        self.pts.append(p)

        # update keys
        for q in self.heap:
            q.updatepred(p)
        heapify(self.heap)
        
        return p

    def isempty(self):
        return len(self.heap) == 0

# General Euclidean Metric
def metric(point1,point2):
    total=0
    for (p1,p2) in zip(point1,point2):
        total=total + (p1-p2)**2
    return math.sqrt(total)

def makeGreedyHeap():
    points=[]
    index=1
    out_points=[]
    with open("InputPoints.txt", "r") as txt:
        out_points.append(Point([float(i) for i in txt.readline().split()],0,None))
        for line in txt:
            p=Point([float(i) for i in line.split()],0.0,out_points[0])
            p.dis=metric(p.pt,out_points[-1].pt)
            points.append(p)
            heapq._siftdown_max(points, 0, len(points)-1)
            index+=1
    while len(points)!=0:
        out_points.append(heapq._heappop_max(points))
        for i in reversed(range(len(points))):
            test_dis=metric(points[i].pt,out_points[-1].pt)
            if test_dis<points[i].dis:
                points[i].pred=out_points[-1]
                points[i].dis=test_dis
                heapq._siftup_max(points,i)
    return out_points
