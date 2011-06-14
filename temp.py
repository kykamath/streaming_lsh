'''
Created on Jun 13, 2011

@author: kykamath
'''

from signature import Signature
from library.vector import Vector, VectorGenerator

def getSignatureForVector(vector, unitRandomVectors): return Signature(vector.dot(rv)>=0 for rv in unitRandomVectors)


numberOfDocuments = 5
#dimension = 10
dimension=2
numberOfRandomVectors = 13

documents = [Vector({1:1,2:2}), Vector({1:1,2:1}), Vector({1:2,2:1}) ,Vector({1:10,2:2}), Vector({1:-5,2:-10})]
#documents = [VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1) for i in range(numberOfDocuments)]
unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1) for i in range(numberOfRandomVectors)]
for doc in documents: 
    print doc
    print getSignatureForVector(doc, unitRandomVectors)