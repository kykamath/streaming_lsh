'''
Created on Jul 5, 2011

@author: kykamath
'''
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

def getLatexForString(str): return '$'+str.replace(' ', '\\ ')+'$'

class CurveFit():
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
