'''
Created on Jun 23, 2011

@author: kykamath
'''
import unittest, sys
sys.path.append('../')
from datetime import datetime, timedelta
from classes import GeneralMethods, TwoWayMap

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
        twoWayMap = TwoWayMap()
        self.assertRaises(TypeError, twoWayMap.set, (5, 1, 2))
        twoWayMap.set(TwoWayMap.MAP_FORWARD, 'a', 'A')
        twoWayMap.set(TwoWayMap.MAP_REVERSE, 'B', 'b')
        self.assertEqual('A', twoWayMap.get(TwoWayMap.MAP_FORWARD, 'a'))
        self.assertEqual('a', twoWayMap.get(TwoWayMap.MAP_REVERSE, 'A'))
        self.assertEqual('B', twoWayMap.get(TwoWayMap.MAP_FORWARD, 'b'))
        self.assertEqual('b', twoWayMap.get(TwoWayMap.MAP_REVERSE, 'B'))
        self.assertEqual({'a':'A', 'b':'B'}, twoWayMap.getMap(twoWayMap.MAP_FORWARD))
        self.assertEqual({'A':'a', 'B':'b'}, twoWayMap.getMap(twoWayMap.MAP_REVERSE))
        
if __name__ == '__main__':
    unittest.main()