import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,'GreedyPermutation')))
from greedypermutation import GreedyPermutation
from point import Point
from metrics import *
import random
 
class TestGreedyPermutation(unittest.TestCase):
     
    def test_naiveGreedyPerm(self):        
        p1 = Point([0])
        p2 = Point([4])
        p3 = Point([8])
        p4 = Point([15])
        p5 = Point([16])
        p6 = Point([18])
        p7 = Point([24])
        p8 = Point([28])
        p9 = Point([32])           
        gp = GreedyPermutation([p1, p2, p3, p4, p5, p6, p7, p8, p9], Euclidean())
        gp.makePerm()
        self.assertListEqual(gp.perm, [p1, p9, p5, p3, p7, p8, p2, p6, p4])
        self.assertEqual(gp.verify(), True)
        num, dim = 1000, 4
        gp2 = GreedyPermutation([Point([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)], Euclidean())
        gp2.makePerm()
        self.assertEqual(gp.verify(), True)
        
     
if __name__ == '__main__':
    unittest.main()
