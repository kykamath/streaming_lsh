'''
Created on Jun 23, 2011

@author: kykamath
'''
import unittest, sys
sys.path.append('../')
from datetime import datetime, timedelta
from classes import GeneralMethods, TwoWayMap, UNIQUE_LIBRARY_KEY

test_time = datetime.now()

class GeneralMethodsTests(unittest.TestCase):
    def test_callMethodEveryInterval(self):
        self.numberOfTimesInMethod, currentTime, final_time = 1, test_time, test_time+timedelta(minutes=60)
        def method(arg1, arg2): 
            self.numberOfTimesInMethod+=1
            self.assertEqual(test_time+timedelta(minutes=15*self.numberOfTimesInMethod), arg2+timedelta(minutes=arg1))
        while currentTime<=final_time:
            GeneralMethods.callMethodEveryInterval(method, timedelta(minutes=15), currentTime, arg1=15, arg2=currentTime)
            currentTime+=timedelta(minutes=1)
    def test_reverseDict(self):
        self.assertEqual({1:'a', 2:'b'}, GeneralMethods.reverseDict({'a':1, 'b':2}))
        self.assertRaises(Exception, GeneralMethods.reverseDict, {'a':1, 'b':1})
        
class TwoWayDictTests(unittest.TestCase):
    def setUp(self):
        self.twoWayMap = TwoWayMap()
        self.assertRaises(TypeError, self.twoWayMap.set, (5, 1, 2))
        self.twoWayMap.set(TwoWayMap.MAP_FORWARD, 'a', 'A')
        self.twoWayMap.set(TwoWayMap.MAP_REVERSE, 'B', 'b')
    def __isValidObject(self): return self.twoWayMap.getMap(TwoWayMap.MAP_REVERSE)==GeneralMethods.reverseDict(self.twoWayMap.getMap(TwoWayMap.MAP_FORWARD))
    def test_basicOperation(self):
        self.assertEqual('A', self.twoWayMap.get(TwoWayMap.MAP_FORWARD, 'a'))
        self.assertEqual('a', self.twoWayMap.get(TwoWayMap.MAP_REVERSE, 'A'))
        self.assertEqual('B', self.twoWayMap.get(TwoWayMap.MAP_FORWARD, 'b'))
        self.assertEqual('b', self.twoWayMap.get(TwoWayMap.MAP_REVERSE, 'B'))
        self.assertEqual({'b': 'B', 'a': 'A'}, self.twoWayMap.getMap(self.twoWayMap.MAP_FORWARD))
        self.assertEqual({'B': 'b', 'A': 'a'}, self.twoWayMap.getMap(self.twoWayMap.MAP_REVERSE))
        self.assertTrue(self.__isValidObject())
    def test_set(self):
        self.twoWayMap.set(TwoWayMap.MAP_FORWARD, 'c', 'A'), self.assertTrue(self.__isValidObject())
        self.twoWayMap.set(TwoWayMap.MAP_REVERSE, 'C', 'b'), self.assertTrue(self.__isValidObject())
        self.twoWayMap.set(TwoWayMap.MAP_FORWARD, 'a', 'D'), self.assertTrue(self.__isValidObject())
        self.twoWayMap.set(TwoWayMap.MAP_REVERSE, 'B', 'd'), self.assertTrue(self.__isValidObject())
    def test_delete(self):
        self.twoWayMap.remove(TwoWayMap.MAP_FORWARD, 'a')
        self.assertEqual({'b': 'B'}, self.twoWayMap.getMap(self.twoWayMap.MAP_FORWARD))
        self.assertEqual({'B': 'b'}, self.twoWayMap.getMap(self.twoWayMap.MAP_REVERSE))
        self.twoWayMap.remove(TwoWayMap.MAP_FORWARD, 'a')
        self.assertTrue(self.__isValidObject())
    def test_length(self):
        self.assertEqual(2, len(self.twoWayMap))
        self.twoWayMap.set(TwoWayMap.MAP_REVERSE, 'C', 'c')
        self.assertEqual(3, len(self.twoWayMap))
    def test_contains(self):
        self.assertTrue(self.twoWayMap.contains(TwoWayMap.MAP_FORWARD, 'a'))
        self.assertFalse(self.twoWayMap.contains(TwoWayMap.MAP_FORWARD, 'A'))
        self.assertTrue(self.twoWayMap.contains(TwoWayMap.MAP_REVERSE, 'B'))
        
if __name__ == '__main__':
    unittest.main()