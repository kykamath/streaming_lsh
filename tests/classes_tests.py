'''
Created on Jun 23, 2011

@author: kykamath
'''
import unittest, sys
sys.path.append('../')
from datetime import datetime, timedelta
from classes import GeneralMethods, TwoWayDict

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

class TwoWayDictTests(unittest.TestCase):
    def test_basicOperation(self):
        twoWayDict = TwoWayDict()
        self.assertRaises(TypeError, twoWayDict.set, (5, 1, 2))
        twoWayDict.set(TwoWayDict.MAP_FORWARD, 'a', 'A')
        twoWayDict.set(TwoWayDict.MAP_REVERSE, 'B', 'b')
        self.assertEqual('A', twoWayDict.get(TwoWayDict.MAP_FORWARD, 'a'))
        self.assertEqual('a', twoWayDict.get(TwoWayDict.MAP_REVERSE, 'A'))
        self.assertEqual('B', twoWayDict.get(TwoWayDict.MAP_FORWARD, 'b'))
        self.assertEqual('b', twoWayDict.get(TwoWayDict.MAP_REVERSE, 'B'))
if __name__ == '__main__':
    unittest.main()