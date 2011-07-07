'''
Created on Jul 5, 2011

@author: kykamath
'''
import unittest
import scipy
from plotting import CurveFit, getCumulativeDistribution

class CurveFitTests(unittest.TestCase):
    def test_curveFitdemo(self):
        real = lambda p, x: p[0] * scipy.exp(-((x-p[1])/p[2])**2) + scipy.rand(100)
        functionToFit = lambda p, x: p[0] * scipy.exp(-((x-p[1])/p[2])**2)
        initialParameters = [5., 7., 3.]
        dataX = scipy.linspace(0, 10, 100)
        dataY = real(initialParameters, dataX)
        cf = CurveFit(functionToFit, initialParameters, dataX, dataY)
        cf.estimate()
        cf.plot()
    def test_exponentialFunctions(self):
        x, p = 85079, [  1.09194452e+03,   1.03448106e+00]
        self.assertTrue(x==int(CurveFit.inverseOfDecreasingExponentialFunction(p, CurveFit.decreasingExponentialFunction(p, x))))
        self.assertTrue(x==int(CurveFit.inverseOfIncreasingExponentialFunction(p, CurveFit.increasingExponentialFunction(p, x))))

class GlobalMethodTests(unittest.TestCase):
    def test_getCumulativeDistribution(self):
        pd = [0.5,0.25, 0.1, 0.1, 0.05]
        cd = [0.5,0.75,0.85,0.95,1.0]
        self.assertEqual(cd,getCumulativeDistribution(pd))

if __name__ == '__main__':
    unittest.main()