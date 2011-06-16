'''
Created on Jun 15, 2011

@author: kykamath
'''

import sys
sys.path.append('../')
from classes import Permutation, Document
from library.vector import Vector, VectorGenerator

def iterateLinesFromFile(filePath):
    for line in open(filePath):
        if not line.startswith('#'): yield line.strip()

    

class OfflineLSHDemo:
    @staticmethod
    def demo():
        wordToDimensionMap = {}
        def createDocumentFromLine(docId, line):
            vector = Vector()
            words = line.split()
            for word in words[1:]:
                if word not in wordToDimensionMap: wordToDimensionMap[word]=len(wordToDimensionMap)
                wordDimension = wordToDimensionMap[word]
                if wordDimension not in vector: vector[wordDimension]=1
                else: vector[wordDimension]+=1
            return Document(docId, vector, clusterType=words[0])
        
        
        dimensions = 52
        signatureLength=13
        numberOfPermutations = 5
        
        unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimensions, 0, 1) for i in range(signatureLength)]
        permutations = [Permutation(signatureLength) for i in range(numberOfPermutations)]
        
        # Build LSH Model
        traningDocumentsMap = {}
        for docId, l in enumerate(iterateLinesFromFile('../data/training.dat')): traningDocumentsMap[docId] = createDocumentFromLine(docId, l)
        
        map(lambda document: document.setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors), traningDocumentsMap.values())
        for permutation in permutations:
            for document in traningDocumentsMap.values(): permutation.addDocument(document)
        
        # Testing the model
        testDocumentsMap = {}
        for docId, l in enumerate(iterateLinesFromFile('../data/test.dat')): testDocumentsMap[docId] = createDocumentFromLine(docId, l)
#        testDocuments = [Document(docId, createVectorFromLine(l)) for docId, l in enumerate(iterateLinesFromFile('../data/test.dat'))]
        map(lambda document: document.setDocumentSignatureUsingUnitRandomVectors(unitRandomVectors), testDocumentsMap.values())
        
        for t in testDocumentsMap.values():
            print map(
                      lambda docId: traningDocumentsMap[docId].clusterType, 
                      reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(t) for permutation in permutations), set())
                      )
            
if __name__ == '__main__':
    OfflineLSHDemo.demo()

