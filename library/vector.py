'''
Created on Jun 14, 2011

@author: kykamath
'''

import math, random

class Vector(dict):
    
    def __init__(self, vectorInitialValues = {}):
        for k,v in vectorInitialValues.iteritems(): self[k]=v
    
    @property
    def dimension(self): return len(self)
    
    def __add__(self, otherVector):
        sumVector = self.copy()
        for k, v in otherVector.iteritems():
            if k in sumVector: sumVector[k]+=v
            else: sumVector[k]=v
        return sumVector
    
    def __sub__(self, otherVector):
        diffVector = self.copy()
        for k, v in otherVector.iteritems():
            if k in diffVector: diffVector[k]-=v
            else: diffVector[k]=v
        return diffVector
    
    def dot(self, otherVector):
        total = 0
        for k in set(self.keys()).union(otherVector.keys()): total+=self.get(k,0)*otherVector.get(k,0)
        return reduce(lambda total, k: total+(self.get(k,0)*otherVector.get(k,0)), set(self.keys()).union(otherVector.keys()),0)
    
    def mod(self): return math.sqrt(sum(x*x for x in self.itervalues()))
    
    def getNormalizedVector(self):
        modValue = self.mod()
        normalizedVector = Vector()
        for k, v in self.iteritems(): normalizedVector[k]=v/modValue
        return normalizedVector
    
class VectorGenerator:
    
    @staticmethod
    def getRandomGaussianUnitVector(dimension, mu, sigma):
        vector = Vector()
        for i in xrange(dimension): vector[i]=random.normalvariate(mu, sigma)
        return vector.getNormalizedVector()

if __name__ == '__main__':
    VectorGenerator.getRandomGaussianUnitVector(10, 0, 1)
        
