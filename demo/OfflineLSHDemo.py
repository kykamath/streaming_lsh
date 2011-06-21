'''
A demo for clustering text document using locality sensitive hashing.

Command to run the demo: python OfflineLSHDemo.py

The training and test documents used in this demo are in the following format:
<cluster_id> <document>
Example:
1 abc def efe tert ertre
2 sdf ertr frf frfe
1 sdfds sdfdsf dsfewf

Created on Jun 15, 2011

@author: kykamath
'''

import sys
sys.path.append('../')
import numpy
from classes import SignaturePermutation, Document, RandomGaussianUnitVector,\
    VectorPermutation
from library.vector import Vector
from library.clustering import EvaluationMetrics
from library.file_io import FileIO
from collections import defaultdict
from operator import itemgetter

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
        
        dimensions = 53
        signatureLength=13
        numberOfPermutations = 5
        
        unitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        vectorPermutations = VectorPermutation.getPermutations(signatureLength, dimensions, unitVector)
        signaturePermutations = [SignaturePermutation(signatureLength) for i in range(numberOfPermutations)]
        
        permutatedUnitVectors = [unitVector.getPermutedVector(r) for r in vectorPermutations]
        
        # Build LSH Model.
        # Read training documents.
        traningDocumentsMap = {}
        for docId, l in enumerate(FileIO.iterateLinesFromFile('../data/train_offline.dat')): traningDocumentsMap[docId] = createDocumentFromLine(docId, l)
        # Construct cluster vectors.
        clusterToDocumentsMap = defaultdict(list)
        for document in traningDocumentsMap.values(): clusterToDocumentsMap[document.clusterType].append(document)
        clusterMap = {}
        for k, v in clusterToDocumentsMap.iteritems(): clusterMap[k]=Document(docId=k, vector=Vector.getMeanVector(v), clusterType=k)
        
        # Create signatures and signaturePermutations for all the clusters.
        map(lambda document: document.setSignatureUsingVectors(permutatedUnitVectors), clusterMap.values())
        for permutation in signaturePermutations:
            for document in clusterMap.values(): permutation.addDocument(document)
        
        # Testing the model.
        # Read testing documents.
        testDocumentsMap = {}
        for docId, l in enumerate(FileIO.iterateLinesFromFile('../data/test_offline.dat')): testDocumentsMap[docId] = createDocumentFromLine(docId, l)
        # Create signatures for test documents
        map(lambda document: document.setSignatureUsingVectors(permutatedUnitVectors), testDocumentsMap.values())
        
        predicted, labels = [], []
        for t in testDocumentsMap.values():
            possibleNearestClusters = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(t) for permutation in signaturePermutations), set())
            predictedClass = max(((clusterType, clusterMap[clusterType].cosineSimilarity(t)) for clusterType in possibleNearestClusters), key=itemgetter(1))
            predicted.append(predictedClass[0])
            labels.append(t.clusterType)
        return EvaluationMetrics.purity(predicted, labels)
            
if __name__ == '__main__':
    print numpy.mean([OfflineLSHDemo.demo() for i in range(10)])
#    print OfflineLSHDemo.demo()

