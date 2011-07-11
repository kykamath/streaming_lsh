'''
Created on Jul 5, 2011

@author: kykamath
'''
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from numpy.ma.core import exp, log

def getLatexForString(str): return '$'+str.replace(' ', '\\ ')+'$'

class CurveFit():
    @staticmethod
    def decreasingExponentialFunction(p, x): 
        ''' Exponential funcion: y = p[0].x^-p[1]    '''
        return p[0]*pow(x, -1*p[1])
    @staticmethod
    def increasingExponentialFunction(p, x): 
        ''' Exponential funcion: y = p[0].x^-p[1]   '''
        return p[0]*pow(x, p[1])
    @staticmethod
    def inverseOfDecreasingExponentialFunction(p, y):
        ''' Inverse exponential funcion: x = e^-(log(y/p[0])/p[1])    '''
        return exp(-1*log(y/p[0])/p[1])
    @staticmethod
    def inverseOfIncreasingExponentialFunction(p, y):
        ''' Inverse exponential funcion: x = e^(log(y/p[0])/p[1])    '''
        return exp(log(y/p[0])/p[1])
    @staticmethod
    def lineFunction(p, x): 
        '''  Line funciton y = p[0]x+p[1]    '''
        return p[0]*x+p[1]
    def __init__(self, functionToFit, initialParameters, dataX, dataY): 
        self.functionToFit, self.initialParameters, self.dataX, self.dataY = functionToFit, initialParameters, dataX, dataY
        if self.functionToFit != None: self.error = lambda p, x, y: self.functionToFit(p, x) - y
    def estimate(self, polyFit=None): 
        if polyFit == None: self.actualParameters, self.success = scipy.optimize.leastsq(self.error, self.initialParameters, args=(self.dataX, self.dataY))
        else: self.actualParameters = np.polyfit(self.dataX, self.dataY, polyFit)
    def errorVal(self):
        xfit=np.polyval(self.actualParameters, self.dataX)
        return scipy.sqrt(sum((self.dataX-xfit)**2)/len(xfit))
    def plot(self, xlabel='', ylabel='', title='', color = 'r'):
        plt.plot(self.dataX, self.dataY, 'o')
        plt.plot(self.dataX, self.functionToFit(self.actualParameters, self.dataX), 'o', color=color)
        plt.xlabel(xlabel), plt.ylabel(ylabel), plt.title(title)
        plt.show()
    def getModeledYValues(self): return self.functionToFit(self.actualParameters, self.dataX)
    @staticmethod
    def getParamsAfterFittingData(x, y, functionToFit, initialParameters):
        cf = CurveFit(functionToFit, initialParameters, x, y)
        cf.estimate()
        return cf.actualParameters
    @staticmethod
    def getYValues(functionToFit, params, x):  return [functionToFit(params, i) for i in x]

def getCumulativeDistribution(probabilityDistribution):
    cumulativeDistribution, cumulative_value = [], 0
    for v in probabilityDistribution: cumulativeDistribution.append(cumulative_value+v); cumulative_value+=v
    return cumulativeDistribution
    