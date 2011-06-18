'''
Created on Jun 16, 2011

@author: kykamath
'''

from library.file_io import FileIO 
from classes import Document, RandomGaussianUnitVector,\
    RandomGaussianUnitVectorPermutation, SignaturePermutation
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
        
        randomGaussianUnitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        randomGaussianUnitVectorPermutations = RandomGaussianUnitVectorPermutation.getPermutations(signatureLength, dimensions, randomGaussianUnitVector)
        signaturePermutations = [SignaturePermutation(signatureLength) for i in range(numberOfPermutations)]
        
        
#        for line in FileIO.iterateLinesFromFile('../data/streaming.dat'):

if __name__ == '__main__':
    OnlineLSHDemo().demo()