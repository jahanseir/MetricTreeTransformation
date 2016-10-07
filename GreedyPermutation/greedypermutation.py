
class GreedyPermutation:
    
    def __init__(self, perm, metric):
        self.perm = []
        self.metric = metric
        for p in perm:
            if p in self.perm: print('point {} is already in the permutation'.format(p))
            else: self.perm.append(p)

    def makePerm(self, start=0):
        for p in self.perm: p.dis = float('inf')
        start = start if start < len(self.perm) else 0
        self.perm[0], self.perm[start] = self.perm[start], self.perm[0]
        self.perm[0].dis, self.perm[0].pred = 0, None
        for i in range(len(self.perm) - 1):
            maxIndex = i + 1
            for j in range(i + 1, len(self.perm)):
                newdist = self.perm[j].dist(self.metric, self.perm[i])[0]
                if newdist < self.perm[j].dis:
                    self.perm[j].dis = newdist
                    self.perm[j].pred = self.perm[i]
                if self.perm[maxIndex].dis < self.perm[j].dis:
                    maxIndex = j
            self.perm[i + 1], self.perm[maxIndex] = self.perm[maxIndex], self.perm[i + 1]
        return self.perm
    
    def verify(self):
        for i in range(1, len(self.perm)):
            if (self.perm[i].dis, self.perm[i].pred) != self.perm[i].dist(self.metric, *[self.perm[j] for j in range(i)]):
                return False
        return True
