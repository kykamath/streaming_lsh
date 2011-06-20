'''
Created on Jun 17, 2011

@author: kykamath
'''

import unittest
from math_modified import isPrime, ModularArithmetic

class MathModifiedTests(unittest.TestCase):
    def test_isPrime(self):
        self.assertFalse(isPrime(1))
        self.assertTrue(isPrime(2))
        self.assertFalse(isPrime(0))
        self.assertTrue(isPrime(13))
        self.assertFalse(isPrime(10))
        self.assertTrue(isPrime(101))
    
class ModularArithmeticTests(unittest.TestCase):
    def test_gcd(self): 
        self.assertEqual(3, ModularArithmetic.gcd(30,21))
        self.assertEqual(1, ModularArithmetic.gcd(7,5))
        self.assertEqual(10, ModularArithmetic.gcd(10,0))
    def test_gcdExtended(self):
        self.assertEqual((3,-11,14), ModularArithmetic.gcdExtended(99, 78))
        self.assertEqual((10,1,0), ModularArithmetic.gcdExtended(10,0))
        
if __name__ == '__main__':
    unittest.main()