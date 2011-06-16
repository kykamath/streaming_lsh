'''
Created on Jun 15, 2011

@author: kykamath
'''

import sys
sys.path.append('../')
from classes import Permutation, Document
from library.vector import Vector, VectorGenerator

def iterateLinesFromFile(filePath):
    for line in open('../data/training.dat'):
        if not line.startswith('#'): yield line.strip()

def createVectorFromLine(line):
    vector = Vector()
    for word in line.split()[1:]:
        if word not in vector: vector[word]=0
        vector[word]+=1
    return vector
    

class OfflineLSHDemo:
    @staticmethod
    def demo():
        dimensions = 52
        signatureLength=13
        numberOfPermutations = 5
        
        unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimensions, 0, 1) for i in range(signatureLength)]
        permutations = [Permutation(signatureLength) for i in range(numberOfPermutations)]
        documents = [Document(docId, createVectorFromLine(l)) for docId, l in enumerate(iterateLinesFromFile('../data/training.dat'))]
        
        
        map(lambda document: document.setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors), documents)
        
        for permutation in permutations:
            for document in documents: permutation.addDocument(document)
        
if __name__ == '__main__':
    OfflineLSHDemo.demo()
