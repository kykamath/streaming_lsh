'''
Created on Jul 5, 2011

@author: kykamath
'''
import unittest
import scipy
from plotting import CurveFit

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

if __name__ == '__main__':
    unittest.main()