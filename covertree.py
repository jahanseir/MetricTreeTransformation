from point import Point
from node import Node
from metrics import *
import copy

class CoverTree:
    def __init__(self, metric, tau=2, cp=1, cc=1):
        if cp > cc or cp <= 0 or cc <= 0:
            raise TypeError('CoverTree.__init__: Values of covering and packing constants do not follow the rules.')
        if tau <= 1:
            raise TypeError('CoverTree.__init__: Value of tau is not greater than one.')
        self.tau, self.cp, self.cc, self.root, self.levels, self.tops = tau, cp, cc, None, dict(), dict()
        self.metric = metric
        self.cr = 3 * self.cc * (self.tau / (self.tau - 1)) ** 2
        self.ntcp = (self.cp * (self.tau - 1) - 2 * self.cc) / (2 * self.tau - 1)
        self.ntcc = (self.cc * self.tau) / (self.tau - 1)
        
    def buildFromGP(self, permutation):
        for p in permutation: self.insert(p, self.findParentFromPred(p))
    
    def findParentFromPred(self, point):
        if point.pred is None: return None
        if point.pred not in self.levels[float('-inf')]:
            raise TypeError('CoverTree.findParentFromPred: Cannot find predecessor of {} in the cover tree'.format(point))
        node = self.levels[float('-inf')][point.pred].par
        level = self.levelof(point.dis)[0]
        if node.level > level: return node
        dist, parent = Node(point).dist(self.metric, *node.par.rel)
        if parent.level == float('-inf'): parent = parent.par
        if (dist == float('inf') or dist > self.cc * self.tau ** parent.level or 
            (parent.level != float('inf') and dist <= self.cp * self.tau ** level)):
            raise TypeError('Cannot find the right parent for point {}'.format(point))
        return parent
    
    def insert(self, point, parNode, findrels=True, preferredlevel=None):
        if parNode is None: 
            node = self.root = self.addJump(point, parNode, float('inf'), findrels)
        else:
            if parNode.point == point: raise TypeError('CoverTree.insert: parent node should have different associated point')   
            levels = self.levelof(point.dist(self.metric, parNode.point)[0])
            level = preferredlevel if preferredlevel is not None and preferredlevel in levels else levels[0]
            if parNode.level <= level or parNode.child().level > level: 
                raise TypeError('CoverTree.insert: level of the node should be between the level of its parent and the level of child of its parent')
            if parNode.level == float('inf'):
                if parNode.child().level < level and parNode.child().level != float('-inf'):                    
                    children = [ch for ch in parNode.ch if ch.point != parNode.point]
                    for child in children: child.detachParent()
                    n1 = self.splitJump(parNode, parNode.child(), parNode.child().level + 1, findrels)
                    for child in children: child.attachParent(n1)
            else:
                parNode = self.splitJump(parNode, parNode.child(), level + 1, findrels)            
            self.splitJump(parNode, parNode.child(), level, findrels)
            node = self.addJump(point, parNode, level, findrels)
        return node
    
    def addToLevel(self, level, point, node):
        if self.levels.get(level) is None: self.levels[level] = {point:node}
        else: self.levels[level][point] = node
        if self.tops.get(point) is None or self.tops[point].level < level: self.tops[point] = node
        
    def deleteFromLevel(self, level, point):
        if self.levels[level].get(point) is not None: del self.levels[level][point]
        if len(self.levels[level]) == 0: del self.levels[level]
        if self.tops.get(point) is not None and self.tops[point].level == level: self.tops[point] = self.tops[point].child()
    
    def addJump(self, point, parNode, level, findrels=True):
        bottom = Node(point, float('-inf'))
        top = Node(point, level).attachChild(bottom).attachParent(parNode)
        if findrels: 
            self.addRelatives(top, top.par)
            self.addRelatives(bottom, bottom.par)
        self.addToLevel(level, point, top)
        self.addToLevel(float('-inf'), point, bottom)
        return top
    
    # top: top node of a jump
    # bottom: bottom node of a jump
    def splitJump(self, top, bottom, level, findrels=True):
        if top.point != bottom.point:
            raise TypeError('CoverTree.splitJump: The top and the bottom node of a jump have different associated points')
        if top.level < level or level < bottom.level:
            raise TypeError('CoverTree.splitJump: The level of a split jump is not in between the levels of top and bottom nodes')
        if level == top.level: return top
        if level == bottom.level: return bottom
        top.detachChild(bottom)
        n1 = Node(top.point, level).attachChild(bottom).attachParent(top)          
        if findrels: self.addRelatives(n1, n1.par)
        self.addToLevel(level, top.point, n1)
        return n1
    
    def addRelatives(self, node, par, updateOthers=True):
        candidates = []
        if par is None: return
        for rel in par.rel:
            candidates += [ch for ch in rel.ch if ch != node]
            self.checkRelative(node, rel, updateOthers)
            self.checkRelative(rel, node, updateOthers)
        while len(candidates) > 0:
            self.checkRelative(node, candidates[0], updateOthers)
            if self.checkRelative(candidates[0], node, updateOthers):
                candidates += candidates[0].ch
            candidates.remove(candidates[0])
             
    def checkRelative(self, node1, node2, updateOthers=True):
        if node2.level <= node1.level < node2.par.level and node1.dist(self.metric, node2)[0] <= self.cr * self.tau ** node1.level:
            existingNode = [item for item in node1.rel if item.point == node2.point]
            if updateOthers:
                if len(existingNode) == 1: node1.rel.remove(existingNode[0])
                elif len(existingNode) > 1:
                    raise TypeError('CoverTree.checkRelative: More than one node with the same point is in rel list of {0}'.format(node1))
                node1.rel.append(node2)
            return True
        return False
 
    def levelof(self, dist):
        try: return list(range(int(math.ceil(math.log(float(dist / self.cc), self.tau)) - 1),
                     int(math.ceil(math.log(dist / self.cp, self.tau)))))
        except ValueError as e:
            print(dist, self.tau, self.cp, self.cc)
            print(math.log(float(dist / self.cc), self.tau))
            print(math.ceil(math.log(float(dist / self.cc), self.tau)))
            print(math.log(float(dist / self.cp), self.tau))
            print(math.ceil(math.log(float(dist / self.cp), self.tau)))
            raise e
    
    def dynamicInsert(self, point):
        if len(self.levels) == 0:
            return self.insert(point, None)
        if point in self.levels[float('-inf')].keys():
            print('The point {} is already in the cover tree'.format(point))
            return
        sortedlevels = sorted(self.uncompressLevels(), reverse=True)
        topLevel = float('inf')
        currentLevelNodes = list(self.levels[topLevel].values())
        return self.recursiveInsert(point, currentLevelNodes, topLevel, sortedlevels)[1]
    
    def recursiveInsert(self, point, currentLevelNodes, level, sortedlevels):
        children = set().union(*[n.ch for n in currentLevelNodes])
        if len(children) == 0 or Node(point).dist(self.metric, *children)[0] > self.cc * self.tau ** (level + 1) / (self.tau - 1): return True, None
        next = sortedlevels[sortedlevels.index(level) + 1]
        nextLevel = [ch.par if ch.level != next else ch 
                     for ch in children if point.dist(self.metric, ch.point)[0] <= self.cc * self.tau ** (level + 1) / (self.tau - 1)]
        found, node = self.recursiveInsert(point, nextLevel, next, sortedlevels)
        if found:
            mindist, minnode = Node(point).dist(self.metric, *currentLevelNodes)
            if mindist <= self.cc * self.tau ** level:
                node = self.insert(point, minnode)
                tobechecked = [ch for rel in node.rel for ch in rel.ch if rel != node]
                for n in tobechecked:
                    tobechecked.extend([ch for ch in n.ch if node.dist(self.metric, ch)[0] < 2 * self.cc * self.tau ** (ch.level + 1) / (self.tau - 1)])
                    if n.point != n.par.point and n.dist(self.metric, n.par)[0] > n.dist(self.metric, node)[0]:
                        self.changeParent(n, node, True)
                return False, node
        return found, node
    
    def dynamicInsert2(self, point):
        if self.root is None:
            return self.insert(point, None)
        if point in self.levels[float('-inf')].keys():
            print('The point {} is already in the cover tree'.format(point))
            return
        node = self.insert(point, self.findParent(point, self.root))
        tobechecked = [ch for rel in node.rel for ch in rel.ch if rel != node]
        for n in tobechecked:
            tobechecked.extend([ch for ch in n.ch if node.dist(self.metric, ch)[0] < 2 * self.cc * self.tau ** (ch.level + 1) / (self.tau - 1)])
            if n.point != n.par.point and n.dist(self.metric, n.par)[0] > n.dist(self.metric, node)[0]:
                self.changeParent(n, node, True)
        return node
    
    def findParent(self, point, node):
        nodes = []
        for ch in node.ch:
            if point.dist(self.metric, ch.point)[0] <= self.cc * self.tau ** (ch.level + 1) / (self.tau - 1):
                n = self.findParent(point, ch)
                if n is not None: nodes.append(n)
        if len(nodes) == 0:
            if point.dist(self.metric, node.point)[0] <= self.cc * self.tau ** node.level: return node
            else: return None
        else:
            return Node(point).dist(self.metric, *nodes)[1]
    
    def augmentRelatives(self):
        for k1 in sorted({k for k in self.levels}, reverse=True):
            for k2 in self.levels[k1]:
                self.addRelatives(self.levels[k1][k2], self.levels[k1][k2].par)
                
    def coarsening(self, k):
        ct = CoverTree(self.metric, self.tau ** k, self.cp, self.cc * self.tau / (self.tau - 1))
        for k1 in sorted([k for k in self.levels if k != float('inf')]):
            for node in self.levels[k1].values():
                ancestor = node
                newancestorlevel = newnodelevel = self.coarserLevel(k, node.level)
                while newancestorlevel == newnodelevel:
                    ancestor = ancestor.par
                    newancestorlevel = self.coarserLevel(k, ancestor.level)
                if ancestor.point == node.point:
                    parlevel = newancestorlevel if node.level == float('-inf') or ancestor.level == float('inf') else newnodelevel + 1
                    ct.findNode(node.point, ct.tops.get(node.point, None), parlevel)
                    ct.findNode(node.point, ct.tops.get(node.point, None), newnodelevel)                    
                else:
                    parent = ancestor
                    for r in [item for item in ancestor.rel if item != ancestor]:
                        x = r
                        if (r.level if r.level == float('-inf') else r.level // k) > newnodelevel + 1:
                            x = self.restrictedNN(node.point, r, k * (node.level // k + 1) - 1)
                        if node.dist(self.metric, x)[0] < node.dist(self.metric, parent)[0]:
                            parent = x
                    parlevel = parent.level if parent.level == float('inf') else newnodelevel + 1
                    q = ct.findNode(parent.point, ct.tops[parent.point], parlevel)[1]
                    ct.findNode(parent.point, ct.tops[parent.point], newnodelevel)               
                    r = ct.findNode(node.point, ct.tops[node.point], newnodelevel)[1]
                    q.attachChild(r)
        ct.root = [v for v in ct.levels[float('inf')].values()][0]
        return ct
    
    def coarserLevel(self, k, level):
        return level if level in [float('inf'), float('-inf')] else level // k
    
    def findNode(self, point, topNode, level):
        node = Node(point, level)
        if topNode is None:
            self.addToLevel(level, point, node)
            return True, node
        top = topNode
        iscreated = True
        while topNode is not None and topNode.level > level: topNode = topNode.child()
        if topNode is None:
            self.addToLevel(level, point, node)
            node.attachParent(top)
        elif topNode.level == level: 
            node = topNode
            iscreated = False
        else:
            ch = topNode
            if topNode.par is not None:
                par = topNode.par
                par.detachChild(topNode).attachChild(node)
            if level != float('inf') and len(topNode.ch) == 1:
                ch = topNode.child()
                self.deleteFromLevel(topNode.level, topNode.point)    
            node.attachChild(ch)
            self.addToLevel(level, point, node)
        return iscreated, node
    
    def bruteForceNN(self, point, root, level):
        closestNodes = [self.bruteForceNN(point, ch, level) for ch in root.ch if ch.level >= level]
        if len(closestNodes) == 0: return root
        return Node(point).dist(self.metric, *closestNodes)[1]
    
    def restrictedNN(self, point, root, level=float('-inf')):
        uncompLevels = self.uncompressLevels()   
        minNode = root
        currentLevel = [root]
        sortedlevels = sorted([k for k in uncompLevels if level <= k <= root.level], reverse=True)    
        for k1 in sortedlevels:
            if sortedlevels.index(k1) == len(sortedlevels) - 1: break
            children = set().union(*[n.ch for n in currentLevel])
            minDist, minNode = Node(point).dist(self.metric, *children)
            currentLevel = []
            for ch in children:
                if ch.point.dist(self.metric, point)[0] <= minDist + self.cc * self.tau ** k1 / (self.tau - 1):
                    currentLevel.append(ch.par if ch.level != sortedlevels[sortedlevels.index(k1) + 1] else ch)
        return minNode
    
    def refining(self, k):
        tau = self.tau ** (1. / k)
        if not tau.is_integer():
            raise TypeError('CoverTree.refining: The scale factor of the finer tree to the power of k should be equal to the scale factor of the given tree')
        ct = CoverTree(self.metric, int(tau), self.cp, self.cc)
        for k1 in sorted([k for k in self.levels if k != float('inf')]):
            for node in self.levels[k1].values():
                top = ct.tops.get(node.point, None)
                if node.point == node.par.point:
                    if node.par.level != float('inf') and (top is None or top.level < k * node.level):
                        parlevel = node.par.level if node.level == float('-inf') else node.level + 1
                        ct.findNode(node.point, top, k * parlevel)
                        ct.findNode(node.point, ct.tops[node.point], k * node.level)                        
                else:
                    parent, parDist = node.par, node.dist(self.metric, node.par)[0]
                    rels = set().union(*[rel.ch for rel in node.par.rel if len(rel.ch) > 1 and rel.child().level == node.level]) - {node}
                    for n in rels:
                        dist = node.dist(self.metric, n)[0]
                        if dist <= ct.cc * ct.tau ** ct.tops[n.point].level and dist < parDist: parent, parDist = n, dist
                    level = ct.levelof(parDist)[0]
                    n1 = ct.findNode(parent.point, ct.tops[parent.point], level + 1)[1]
                    ct.findNode(parent.point, ct.tops[parent.point], level)
                    n2 = ct.findNode(node.point, ct.tops[node.point], level)[1]
                    n1.attachChild(n2)
                    for n in rels:
                        top = ct.tops[n.point]
                        dist = n2.dist(self.metric, top)[0]
                        if top.par is not None and top.dist(self.metric, top.par)[0] > dist and dist <= ct.cc * ct.tau ** level:
                            ct.changeParent(top, n2, False)
        root = [v for v in ct.levels[sorted(ct.levels, reverse=True)[0]].values()][0]
        if root.level != float('inf'):            
            ct.deleteFromLevel(root.level, root.point)
            root.level = float('inf')
            ct.addToLevel(root.level, root.point, root)
        ct.root = root
        return ct
    
    def changeParent(self, node, newparent, changerels):
        n = node.par.child()
        node.detachParent()
        level = self.levelof(node.dist(self.metric, newparent)[0])[0]
        if level < node.level:
            self.deleteFromLevel(node.level, node.point)
        child = None
        for i in range(2):
            par = n.par
            if len(n.ch) == 1 and par is not None and len(par.ch) == 1:
                child = n.child()
                n.detachParent().detachChild(child)
                par = par.attachChild(child)                
                self.deleteFromLevel(n.level, n.point)
            n = par
        createdtop, newparent = self.findNode(newparent.point, newparent, level + 1)
        createdbottom = self.findNode(newparent.point, newparent, level)[0]
        node.attachParent(newparent)
        if changerels:
            if child is not None:
                self.addRelatives(child, child.par, True)
            if createdtop:
                self.addRelatives(newparent, newparent.par, True)
            if createdbottom:
                self.addRelatives(newparent.child(), newparent, True)
    
    def uncompressLevels(self):
        if len(self.levels) == 0: return {}
        prevLevel = float('inf')
        uncompLevels = {prevLevel:[v for v in self.levels[prevLevel].values()]}
        for k1 in sorted([k for k in self.levels if k != float('inf')], reverse=True):
            prev = copy.copy(uncompLevels[prevLevel])
            for n1 in self.levels[k1].values():
                for n2 in prev:
                    if n1.point == n2.point:
                        prev.remove(n2)
                        break
                uncompLevels[k1] = [n1] if uncompLevels.get(k1) is None else uncompLevels[k1] + [n1]
            uncompLevels[k1] += prev
            prevLevel = k1
        return uncompLevels
    
    def verifyRelatives(self):
        uncompLevels = self.uncompressLevels()
        for k1 in sorted({k for k in uncompLevels if k != float('inf') and k != float('-inf')}, reverse=True):
            for n1 in uncompLevels[k1]:
                for n2 in uncompLevels[k1]:
                    if n1.level == k1 and n1.dist(self.metric, n2)[0] <= self.cr * self.tau ** k1 and n2.point not in [v.point for v in n1.rel]:
                        return False
        return True
      
    def isHierarchical(self):
        for k1 in sorted({k for k in self.levels if k != float('-inf')}, reverse=True):
            for n in self.levels[k1].values():
                if (n.point not in [ch.point for ch in n.ch] or len({ch.level for ch in n.ch}) > 1 or 
                    (len(n.ch) > 1 and n.level != float('inf') and n.child().level + 1 < n.level) or
                    (n.level != float('inf') and len(n.ch) == 1 and len(n.par.ch) == 1)):
                    return False
        return True
    
    def isCoverTree(self, closestPar=True):
        if not self.isHierarchical(): return False
        uncompLevels = self.uncompressLevels()
        for k1 in sorted({k for k in uncompLevels if k != float('inf') and k != float('-inf')}, reverse=True):
            for n1 in uncompLevels[k1]:
                for n2 in uncompLevels[k1]:
                    if (n1 != n2 and (n1.dist(self.metric, n2)[0] <= self.cp * self.tau ** k1 or 
                    n1.dist(self.metric, n1.par)[0] > self.cc * self.tau ** n1.par.level)):
                        return False
                    if closestPar:
                        for child in n1.ch:
                            if child.dist(self.metric, n2)[0] < child.dist(self.metric, n1)[0]: 
                                return False
        return True
    
    def isNetTree(self):
        if self.tau <= 1 + 2 * self.cc / self.cp or not self.isHierarchical(): return False
        self.root.findLeaves()
        for k1 in sorted({k for k in self.levels if k != float('inf') and k != float('-inf')}, reverse=True):
            for k2 in self.levels[k1]:
                root = self.levels[k1][k2]
                for point in root.leaves:
                    if root.point.dist(self.metric, point)[0] > self.ntcc * self.tau ** root.level: return False
                for point in self.root.leaves - root.leaves:
                    if root.point.dist(self.metric, point)[0] <= self.ntcp * self.tau ** root.level: return False
        return True        
    
    def importFrom(self, path, addrels=True):
        f = open(path)
        section = 0
        d = dict()
        for line in f:
            if ',' in line: 
                section += 1
                continue
            elems = line.split()
            if section == 0:
                self.metric = eval(elems[0])()
            elif section == 1:
                self.tau = int(elems[0])
                self.cp = float(elems[1])
                self.cc = float(elems[2])
            elif section == 2: d[elems[0]] = Point([int(elems[index]) for index in range(1, len(elems))])
            elif section == 3:
                level = float(elems[0]) if 'inf' in elems[0] else int(elems[0])
                parNode = None
                parFound = False
                if level != float('inf'):
                    for k1 in sorted({k for k in self.levels if k > level}):
                        for k2 in self.levels[k1]:
                            if self.levels[k1][k2].point == d[elems[2]]:
                                parNode = self.levels[k1][k2]
                                parFound = True
                                break
                        if parFound: break
                if parNode is None or parNode.point != d[elems[1]]: self.insert(d[elems[1]], parNode, addrels, level)
            else: raise TypeError('CoverTree.importFrom: The input file does not follow the correct format.')
        f.close()
        
    def exportTo(self, path):
        f = open(path, 'w')
        d = dict()
        i = 0
        f.write('{}\n,\n{} {} {}\n,\n'.format(self.metric, self.tau, self.cp, self.cc))
        for k in self.levels[float('-inf')]:
            f.write('{} {}\n'.format(i, ' '.join([str(item) for item in self.levels[float('-inf')][k].point.pt])))
            d[k] = i
            i += 1
        f.write(',\n')
        for k1 in sorted({k for k in self.levels if k != float('-inf')}, reverse=True):
            for k2 in self.levels[k1]:
                if k1 == float('inf'): f.write('{0} {1}\n'.format(k1, d[k2]))
                else: f.write('{} {} {}\n'.format(k1, d[k2], d[self.levels[k1][k2].par.point]))
        f.close()
        
    def report(self):
        totalCompressionNo = compressionNo = nodeNo = 0
        pointNo = len(self.levels[float('-inf')].values())
        for level in self.levels:
            for node in self.levels[level].values():
                if node.par is not None and node.par.level > node.level + 1:
                    totalCompressionNo += 1
                    if level != float('-inf') and node.par.level != float('inf'): compressionNo += 1
                nodeNo += 1
        print('CT({},{},{}) has {} points, {} nodes, {} compressed nodes excluding inf and -inf, and {} levels'
              .format(self.tau, self.cp, self.cc, pointNo, nodeNo, compressionNo, len(self.levels)))
                


