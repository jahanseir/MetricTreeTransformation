from point import Point
from metrics import Euclidean
from heapq import heapify, heappop, heappush

class CPoint(Point):
    def __init__(self, pt, metric=Euclidean()):
        Point.__init__(self, pt)
        self.metric = metric
        self.neighbors = [self]
        self.rnn = []
        self.radius = 0

    # overridden: does not change key
    def updatePred(self, pt):
        self.pred = pt
        pt.radius = self.dist(self.metric, pt)[0]

    def setCenterDist(self):
        self.dis = 0 if len(self.rnn) == 0 else self.rnn[0].dis

    # adds point to self.rnn in a heap invariant
    def addRNN(self, point):
        point.dis = self.dist(self.metric, point)[0]
        heappush(self.rnn, point)
        
    def rnnPeek(self):
        return self.rnn[0]

    def rnnPop(self):
        return heappop(self.rnn)
    
    def rnnIsEmpty(self):
        return len(self.rnn) == 0
    
    # if RNN of Pt are closer to self, places RNN in self.rnn
    def newCenter(self, pt):
        i = 0
        while i < len(pt.rnn):
            rnbr = pt.rnn[i]
            d = self.dist(self.metric, rnbr)[0]
            if  d < rnbr.dis:
                pt.rnn.remove(rnbr)
                rnbr.dis = d
                heappush(self.rnn, rnbr)
                i -= 1
            i += 1
        if len(pt.rnn) != 0:
            heapify(pt.rnn)
            pt.setCenterDist()

