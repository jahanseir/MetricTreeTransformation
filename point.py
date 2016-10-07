import math
from metrics import Euclidean

class Point:

    def __init__(self, pt, dis=0, pred=None):
        self.pt = pt
        self.dis = dis
        self.pred = pred
        
    def dist(self, metric, *others):
        return metric.dist(self, *others)
        
    @staticmethod
    def importFrom(path):
        points = []
        with open(path) as f:
            for line in f:
                points.append(Point([int(coord) if float(coord).is_integer() else float(coord) for coord in line.split()]))
        return points
    
    @staticmethod
    def exportTo(path, points):
        with open(path, 'w') as f:
            for point in points: f.write(' '.join([str(coord) for coord in point.pt]) + '\n')
    
    def __sub__(self, other):
        return [self.pt[i] - other.pt[i] for i in range(min(len(self.pt), len(other.pt)))]
    
    def __lt__(self, other):
        return self.dis > other.dis
        
    def __str__(self):
        return 'pt: {} dis: {} pre: ( {} )'.format(self.pt, self.dis, self.pred)
    
    def __eq__(self, other):
        return self.pt == other.pt
               
    def __hash__(self):
        return hash(tuple(self.pt))
