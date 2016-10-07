import unittest
from point import Point
from metrics import *
import random

class TestPoint(unittest.TestCase):
    
    def test_init(self):
        Point([3, 4])
        Point([0, 0])
        Point([1.23, -3.134], Euclidean())
        Point([0, 0, 3, 1241, 235402], Euclidean())
        
    def test_dist(self):
        p1 = Point([3, 4])
        p2 = Point([0, 0])
        metric = Euclidean()
        self.assertEqual(p1.dist(metric, p2), (5.0, p2))
        p3 = Point([6, 8])
        self.assertEqual(p1.dist(metric, p3), (5.0, p3))
        p4 = Point([0, 5])
        p5 = Point([-12, 0])
        self.assertEqual(p4.dist(metric, p5), (13.0, p5))
        self.assertEqual(p2.dist(metric, p1, p3, p4, p5), (5, p1))
        self.assertEqual(metric.counter, 7)
        metric.counter = 0
        self.assertEqual(p5.dist(metric, p1, p2, p3, p4), (12, p2))
        self.assertEqual(p5.dist(metric, p1, p3, p4), (13, p4))
        self.assertEqual(metric.counter, 7)
        
        metric = Manhattan()
        p = Point([3, 4])
        q = Point([0, 0])
        self.assertEqual(p.dist(metric, q), (7, q))
        p = Point([0, 5])
        q = Point([-12, 0])
        self.assertEqual(p.dist(metric, q), (17, q))
        self.assertEqual(metric.counter, 2)
        
        metric = LInfinity()
        p = Point([3, 4])
        q = Point([0, 0])
        self.assertEqual(p.dist(metric, q), (4, q))
        p = Point([0, 5])
        q = Point([-12, 0])
        self.assertEqual(p.dist(metric, q), (12, q))
        self.assertEqual(metric.counter, 2)
      
    def test_importFrom(self):
        input = [Point([0, 2 ** i]) for i in range(8)]
        points = Point.importFrom('01.txt')
        for p in points: self.assertIn(p, input)
        
    def test_exportTo(self):
        input = [Point([0, 2 ** i]) for i in range(8)]
        Point.exportTo('01.txt', input)
        points = Point.importFrom('01.txt')
        for p in points: self.assertIn(p, input)

if __name__ == '__main__':
    unittest.main()
