'''
Created on Jun 17, 2011

@author: kykamath
'''

import unittest
from math_modified import isPrime, ModularArithmetic, exponentialDecay,\
    DateTimeAirthematic, getLargestPrimeLesserThan,\
    getSmallestPrimeNumberGreaterThan
from datetime import datetime

class MathModifiedTests(unittest.TestCase):
    def test_isPrime(self):
        self.assertFalse(isPrime(1))
        self.assertTrue(isPrime(2))
        self.assertFalse(isPrime(0))
        self.assertTrue(isPrime(13))
        self.assertFalse(isPrime(10))
        self.assertTrue(isPrime(101))
    def test_exponentialDecay(self):
        self.assertEqual(16, exponentialDecay(currentValue=16, decayCoefficient=1, timeDifference=2))
        self.assertEqual(8, exponentialDecay(currentValue=16, decayCoefficient=0.5, timeDifference=1))
        self.assertEqual(4, exponentialDecay(currentValue=16, decayCoefficient=0.5, timeDifference=2))
        self.assertEqual(0, exponentialDecay(currentValue=16, decayCoefficient=0, timeDifference=2))
        self.assertEqual(16, exponentialDecay(currentValue=16, decayCoefficient=0, timeDifference=0))
    def test_getLargestPrimeLesserThan(self):
        self.assertEqual(5, getLargestPrimeLesserThan(6))
        self.assertEqual(13, getLargestPrimeLesserThan(15))
    def test_getSmallestPrimeNumberGreaterThan(self):
        self.assertEqual(7, getSmallestPrimeNumberGreaterThan(7))
        self.assertEqual(11, getSmallestPrimeNumberGreaterThan(8))

class ModularArithmeticTests(unittest.TestCase):
    def test_gcd(self): 
        self.assertEqual(3, ModularArithmetic.gcd(30,21))
        self.assertEqual(1, ModularArithmetic.gcd(7,5))
        self.assertEqual(10, ModularArithmetic.gcd(10,0))
    def test_gcdExtended(self):
        self.assertEqual((3,-11,14), ModularArithmetic.gcdExtended(99, 78))
        self.assertEqual((10,1,0), ModularArithmetic.gcdExtended(10,0))

class DateTimeAirthematicTests(unittest.TestCase):
    def test_getDifferenceInTimeUnits(self):
        self.assertEqual(1, DateTimeAirthematic.getDifferenceInTimeUnits(datetime(2010,10,12,10,31), datetime(2010,10,12,10,30), 60))
        self.assertEqual(4, DateTimeAirthematic.getDifferenceInTimeUnits(datetime(2010,10,12,10,31), datetime(2010,10,12,10,30), 15))
        self.assertEqual(1, DateTimeAirthematic.getDifferenceInTimeUnits(datetime(2010,10,12,10,30), datetime(2010,10,12,10,46), 15*60))
        
if __name__ == '__main__':
    unittest.main()