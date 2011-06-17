'''
Created on Jun 13, 2011

@author: kykamath
'''

#from classes import Document, Permutation
#from library.vector import Vector, VectorGenerator
#
#numberOfDocuments = 5
#dimension=2
#lengthOfSignature = 13
#numberOfPermutations = 5
#
##documents = [Document(Vector({1:1,2:2})), Document(Vector({1:5,2:1})), Document(Vector({1:-2,2:1})),
##             Document(Vector({1:10,2:2})), Document(Vector({1:-5,2:-10}))]
#documents = dict((i, Document(i, VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1))) for i in xrange(numberOfDocuments))
#unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension, 0, 1) for i in range(lengthOfSignature)]
#permutations = [Permutation(lengthOfSignature) for i in range(numberOfPermutations)]
#for doc in documents: documents[doc].setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors)
#
##    print doc, doc.setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors), doc.signature
#
#for permutation in permutations: 
#    for docId in documents: permutation.documentSignatures[docId] = documents[doc].signature.permutate(permutation)
#    print permutation.documentSignatures

#
#from numpy import arange,sqrt, random, linalg
#from multiprocessing import Pool
#
#counter = 0
#def cb(r):
#    global counter
#    print counter, r
#    counter +=1
#    
#def det(M):
#    return linalg.det(M)
#
#po = Pool()
#for i in xrange(1,300):
#    j = random.normal(1,1,(100,100))
#    po.apply_async(det,(j,),callback=cb)
#po.close()
#po.join()
#print counter

import numpy
import math
def prime(upto=100000):
    return filter(lambda num: (num % numpy.arange(2,1+int(math.sqrt(num)))).all(), range(2,upto+1))

print prime()