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
documents = dict((i, Document(i, VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1))) for i in xrange(numberOfDocuments))
unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1) for i in range(lengthOfSignature)]
permutations = [Permutation(lengthOfSignature) for i in range(numberOfPermutations)]
for doc in documents: documents[doc].setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors)

#    print doc, doc.setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors), doc.signature

for permutation in permutations: 
    for docId in documents: permutation.documentSignatures[docId] = documents[doc].signature.permutate(permutation)
    print permutation.documentSignatures
