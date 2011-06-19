'''
Created on Jun 17, 2011

@author: kykamath
'''

import unittest
from math_modified import isPrime, gcd

class MathModifiedTests(unittest.TestCase):
    def test_isPrime(self):
        self.assertFalse(isPrime(1))
        self.assertTrue(isPrime(2))
        self.assertFalse(isPrime(0))
        self.assertTrue(isPrime(13))
        self.assertFalse(isPrime(10))
        self.assertTrue(isPrime(101))
    
    def test_gcd(self): self.assertEqual(3, gcd(30,21))
        
if __name__ == '__main__':
    unittest.main()