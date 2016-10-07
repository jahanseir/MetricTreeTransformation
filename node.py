
class Node:
    def __init__(self, point, level=None):
        self.point = point
        self.level = level
        self.par = None
        self.ch = []
        self.rel = [self]
        self.leaves = {point}
        
    def attachChild(self, child):
        if self != child and child not in self.ch:
            parent = child.par = self
            if self.point == child.point: self.ch.insert(0, child)
            else: self.ch.append(child)
        return self
    
    def detachChild(self, child):
        if child in self.ch:
            parent = child.par
            child.par = None
            self.ch.remove(child)
        return self
       
    def attachParent(self, parent):
        if parent is not None and self != parent and self not in parent.ch:
            _parent = self.par = parent
            if self.point == parent.point: parent.ch.insert(0, self)
            else: parent.ch.append(self)
        return self
        
    def detachParent(self):
        if self.par is not None:
            parent = self.par
            self.par.ch.remove(self)
            self.par = None
        return self    
    
    def child(self):
        if not self.isleaf():
            return self.ch[0]
        else:
            return None
    
    def verifyLeaves(self):
        if len(self.ch) == 0: return {self.point}, True
        allLeaves = set()
        for ch in self.ch:
            leaves, correct = ch.verifyLeaves()
            if not correct or ch.leaves != leaves: return set(), False
            allLeaves |= leaves
        return (allLeaves, True) if self.leaves == allLeaves else (set(), False)
    
    def findLeaves(self):
        leaves = [ch.findLeaves() for ch in self.ch]
        if len(leaves) > 0: self.leaves = set().union(*leaves)
        return self.leaves
    
    def isleaf(self):
        return len(self.ch) == 0

    def dist(self, metric, *others):
        dist, point = self.point.dist(metric, *[n.point for n in others])
        for n in others:
            if n.point == point:
                return dist, n
        raise TypeError('Node.dist: there is not any nodes with the closest point as its associated point')
    
    def __eq__(self, other):
        return self.point == other.point and self.level == other.level
    
    def __str__(self):
        return 'point: {0} level: {1}'.format(self.point.pt, self.level) 
    
    def __hash__(self):
        return hash((tuple(self.point.pt), self.level))               
