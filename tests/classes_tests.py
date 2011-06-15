'''
Created on Jun 14, 2011

@author: kykamath
'''
import unittest
from signature import Signature, Permutation

class SignatureTests(unittest.TestCase):
    
    def test_initialization(self):
        sgnt = Signature('1001011')
        self.assertEqual(sgnt.count(), 4)
        sgnt = Signature()
        self.assertEqual(sgnt.count(), 0)
        
    def test_permutate(self):
        sgnt = Signature('1001011')
        self.assertTrue(sgnt.count()==sgnt.permutate(Permutation(7)).count())
        
class PermutationTests(unittest.TestCase):
    
    def setUp(self):
        self.pm = Permutation(13)
    
    def test_initialization(self):
        self.assertTrue(self.pm.a<self.pm.p and self.pm.b<self.pm.p)
        self.assertTrue(self.pm.a%2!=0)
    
    def test_permutationFunction(self):
        l = [self.pm.apply(i) for i in range(self.pm.p)]
        self.assertEqual(sorted(l), range(self.pm.p))
        
if __name__ == '__main__':
    unittest.main()