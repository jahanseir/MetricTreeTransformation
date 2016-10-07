import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,'GreedyPermutation')))
from CPoint import CPoint
from CHeap import CHeap
from greedypermutation import GreedyPermutation
from metrics import *
import random
from point import Point

class TestCHeap(unittest.TestCase):
    
    def test_makePerm(self):
        p1 = CPoint([0])
        p2 = CPoint([64])
        p3 = CPoint([45])
        p4 = CPoint([16])
        p5 = CPoint([8])
        p6 = CPoint([4])
        p7 = CPoint([2])
        p8 = CPoint([1])
        h = CHeap([p1, p2, p3, p4, p5, p6, p7, p8], Euclidean())
        perm = h.makePerm()
        self.assertEqual(len(h.heap), 0)
        self.assertEqual(len(h.perm), 8)
        self.assertListEqual(perm, [p1, p2, p3, p4, p5, p6, p7, p8])
#         
        num, dim = 200, 2
        metric = Euclidean()
        cpoints = [CPoint([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)]
#         points=Point.importFrom('c:\\errorCHeap.txt')
#         cpoints=[CPoint(p.pt) for p in points]
        perm = CHeap(cpoints, metric).makePerm()
        print(metric.counter)
        gp = GreedyPermutation(perm, Euclidean())
        if not gp.verify(): Point.exportTo('errorCHeap.txt', cpoints)
        self.assertEqual(gp.verify(), True)
        
if __name__ == '__main__':
    unittest.main()
