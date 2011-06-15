'''
Created on Jun 13, 2011

@author: kykamath
'''

from classes import Document, Permutation
from library.vector import Vector, VectorGenerator

numberOfDocuments = 5
dimension=2
lengthOfSignature = 13
numberOfPermutations = 5

#documents = [Document(Vector({1:1,2:2})), Document(Vector({1:5,2:1})), Document(Vector({1:-2,2:1})),
#             Document(Vector({1:10,2:2})), Document(Vector({1:-5,2:-10}))]
documents = [Document(VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1)) for i in range(numberOfDocuments)]
unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1) for i in range(lengthOfSignature)]
permutations = [Permutation(lengthOfSignature) for i in range(numberOfPermutations)]
for doc in documents: doc.initializeSignatureForVector(unitRandomVectors)

#    print doc, doc.initializeSignatureForVector(unitRandomVectors), doc.signature

for p in permutations: print p