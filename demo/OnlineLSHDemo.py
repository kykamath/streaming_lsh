'''
A demo for clustering text document using locality sensitive hashing.

Command to run the demo: python OnlineLSHDemo.py

The input document used in this demo is in the following format:
<cluster_id> <document>
Example:
1 abc def efe tert ertre
2 sdf ertr frf frfe
1 sdfds sdfdsf dsfewf

Created on Jun 16, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import numpy
from library.file_io import FileIO 
from classes import Document, RandomGaussianUnitVector,\
    VectorPermutation, SignaturePermutation, Cluster
from library.vector import Vector
from operator import itemgetter
from itertools import combinations
from library.clustering import EvaluationMetrics

class OnlineLSHDemo:
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
            return Document(docId, vector, clusterId=words[0])
        
        dimensions = 53
        signatureLength=13
        numberOfPermutations = 5
        thresholdForDocumentToBeInACluster = 0.2
        
        unitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        vectorPermutations = VectorPermutation.getPermutations(signatureLength, dimensions, unitVector)
        signaturePermutations = [SignaturePermutation(signatureLength) for i in range(numberOfPermutations)]
        
        # Process the stream.
        docId = 0
        clusterMap, docsToOriginalClusterMap = {}, {}
        for line in FileIO.iterateLinesFromFile('../data/streaming.dat'):
            document = createDocumentFromLine(docId, line)
            docsToOriginalClusterMap[docId] = document.clusterId
            docId+=1
            document.setSignatureUsingVectorPermutations(unitVector, vectorPermutations)
            # Get nearest cluster is different permutations
            # If nearest clusters exist AND above threshold,
            #    Update the nigbors mean with the document
            #    Mark the document to belong to a cluster id
            # If no neighbors,
            #    Create a new cluster. Add the document as new cluster
            #    Add the cluster to all permutations.
            predictedCluster = None
            possibleNearestClusters = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in signaturePermutations), set())
            if possibleNearestClusters: predictedCluster = max(((clusterId, clusterMap[clusterId].cosineSimilarity(document)) for clusterId in possibleNearestClusters), key=itemgetter(1))
            if predictedCluster and predictedCluster[1]>=thresholdForDocumentToBeInACluster:
                clusterMap[predictedCluster[0]].addDocument(document)
            else:
                newCluster = Cluster(document)
                newCluster.setSignatureUsingVectorPermutations(unitVector, vectorPermutations)
                for permutation in signaturePermutations: permutation.addDocument(newCluster)
                clusterMap[newCluster.clusterId] = newCluster
        clusterLabels = []
        for k, cluster in clusterMap.iteritems(): clusterLabels.append([docsToOriginalClusterMap[doc.docId] for doc in cluster.iterateDocumentsInCluster()])
#        print clusterLabels
        return EvaluationMetrics.getValueForClusters(clusterLabels, EvaluationMetrics.purity)
        
if __name__ == '__main__':
    print numpy.mean([OnlineLSHDemo.demo() for i in range(10)])
#    print OnlineLSHDemo().demo()