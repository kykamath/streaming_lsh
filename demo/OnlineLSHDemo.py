'''
Created on Jun 16, 2011

@author: kykamath
'''

from library.file_io import FileIO 
from classes import Document, RandomGaussianUnitVector,\
    VectorPermutation, SignaturePermutation
from library.vector import Vector

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
            return Document(docId, vector, clusterType=words[0])
        
        dimensions = 53
        signatureLength=13
        numberOfPermutations = 5
        
        unitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        vectorPermutations = VectorPermutation.getPermutations(signatureLength, dimensions, unitVector)
        signaturePermutations = [SignaturePermutation(signatureLength) for i in range(numberOfPermutations)]
        
        # Process the stream.
        docId = 0
        for line in FileIO.iterateLinesFromFile('../data/streaming.dat'):
            document = createDocumentFromLine(docId, line)
            document.setSignatureUsingVectorPermutations(unitVector, vectorPermutations)
#            for permutation in signaturePermutations:
#                possibleNearestClusters = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in signaturePermutations), set())
#                if not possibleNearestClusters: 
            docId+=1

if __name__ == '__main__':
    OnlineLSHDemo().demo()