import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,'GreedyPermutation')))
from CPoint import CPoint

class TestCPoint(unittest.TestCase):
    
    def test_init(self):
        CPoint([3,4])
        CPoint([0,0])
        CPoint([1.23,-3.134])
        CPoint([0,0,3, 1241, 235402])

    def test_addRNN(self):
        tpoint = CPoint([0,3])
        a = CPoint([0,2])
        b = CPoint([1,0])
        c = CPoint([3,5])
        tpoint.addRNN(b)
        tpoint.addRNN(a)
        tpoint.addRNN(c)
        self.assertEqual(len(tpoint.rnn),3)

    def test_rnn_Peek_and_Pop(self):
        tpoint = CPoint([0,3])
        a = CPoint([0,2])
        b = CPoint([1,0])
        c = CPoint([3,5])
        tpoint.addRNN(b)
        tpoint.addRNN(a)
        tpoint.addRNN(c)
        peek = tpoint.rnnPeek()
        self.assertEqual(peek,tpoint.rnnPop())
        self.assertNotEqual(peek,tpoint.rnnPeek())

    def test_farthest(self):
        tpoint = CPoint([0,3])
        a = CPoint([0,2])
        b = CPoint([1,0])
        c = CPoint([3,5])
        tpoint.addRNN(b)
        tpoint.addRNN(a)
        tpoint.addRNN(c)
        self.assertEqual(tpoint.rnnPeek(),c)
        
    def test_newCenter(self):
        tpoint = CPoint([0,3])
        point = CPoint([0,0])
        a = CPoint([0,2])
        b = CPoint([1,0])
        c = CPoint([3,5])
        point.addRNN(b)
        point.addRNN(a)
        point.addRNN(c)
        tpoint.newCenter(point)
        self.assertEqual(len(tpoint.rnn),2)
        self.assertEqual(len(point.rnn),1)
        self.assertEqual(tpoint.rnnPeek(),c)
        self.assertEqual(point.rnnPeek(),b)
    
if __name__ == '__main__':
    unittest.main()
