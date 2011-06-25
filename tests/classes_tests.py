'''
Created on Jun 23, 2011

@author: kykamath
'''
import unittest, sys
sys.path.append('../')
from datetime import datetime, timedelta
from classes import GeneralMethods

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
if __name__ == '__main__':
    unittest.main()