import math
from abc import ABCMeta, abstractmethod

class Metric:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.counter = 0

    def dist(self, first, *others):
        if len(others) == 0: raise TypeError("Euclidean.dist: this method should have at least two arguments")
        self.counter += 1
        minDist, minPoint = self.distance(first, others[0]), others[0]
        for i in range(1, len(others)):
            self.counter += 1
            currDist = self.distance(first, others[i])
            if currDist < minDist: minDist, minPoint = currDist, others[i]
        return minDist, minPoint
    
    @abstractmethod
    def distance(self, first, second): pass
    
    def __str__(self):
        return type(self).__name__

class Euclidean(Metric):
    def distance(self, first, second):
        return math.sqrt(sum([x_i ** 2 for x_i in first - second]))

class Manhattan(Metric):
    def distance(self, first, second):
        return sum([abs(x_i) for x_i in first - second])
        
class LInfinity(Metric):
    def distance(self, first, second):
        return max([abs(x_i) for x_i in first - second])
         

