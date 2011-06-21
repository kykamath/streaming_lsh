'''
Created on Jun 14, 2011

@author: kykamath
'''
import random
from bitarray import bitarray
from Bio import trie
from library.vector import VectorGenerator, Vector
from library.math_modified import isPrime, ModularArithmetic

class SignatureTrie:
    @staticmethod
    def getNearestSignatureKey(trie, signature):
        digitReplacement = {'0': '1', '1': '0'}
        targetKey, iteratingKey = signature.to01(), ''
        for i in range(len(targetKey)):
            iteratingKey+=targetKey[i]
            if not trie.has_prefix(iteratingKey): iteratingKey=iteratingKey[:-1]+digitReplacement[targetKey[i]]
        return iteratingKey

class Signature(bitarray):
    def permutate(self, permutation): return Signature([self[permutation.applyFunction(x)] for x in xrange(len(self))])

class Permutation(object):
    def __init__(self, maximumValue): 
        if not isPrime(maximumValue): raise Exception('Maximum value should be prime')
        self.p, self.a, self.b = maximumValue, random.choice(range(maximumValue)[3::2]), random.choice(range(maximumValue))
    def applyFunction(self, x): return (self.a*x+self.b)%self.p
    def __eq__(self, other): return self.a==other.a and self.b==other.b and self.p==other.p
    def __str__(self): return 'p: %s, a: %s, b: %s'%(self.p, self.a, self.b)
    
class SignaturePermutation(Permutation):
    def __init__(self, signatureLength): 
        super(SignaturePermutation, self).__init__(signatureLength)
        self.signatureTrie = trie.trie()
    def addDocument(self, document):
        permutedDocumentSignatureKey = document.signature.permutate(self).to01()
        if self.signatureTrie.has_key(permutedDocumentSignatureKey): self.signatureTrie[permutedDocumentSignatureKey].add(document.docId)
        else: self.signatureTrie[permutedDocumentSignatureKey] = set([document.docId])
    def getNearestDocuments(self, document):
        permutedDocumentSignature = document.signature.permutate(self)
        nearestSignatureKey=SignatureTrie.getNearestSignatureKey(self.signatureTrie, permutedDocumentSignature)
        return self.signatureTrie[nearestSignatureKey]
    
class Document(Vector):
    def __init__(self, docId, vector, clusterType = None):
        super(Document, self).__init__(vector)
        self.docId, self.clusterType = docId, clusterType
#        self.docId, self.vector, self.clusterType = docId, vector, clusterType
    def setSignatureUsingVectors(self, vectors): self.signature = Signature(self.dot(v)>=0 for v in vectors)
    def setSignatureUsingVectorPermutations(self, vector, vectorPermutations):
        self.signature = Signature('')
        for vp in vectorPermutations:
            total = sum(self[dimension]*vector[vp.applyFunction(dimension)] for dimension in self)
            self.signature.append(total>=0)
    def __str__(self): return str(self.__dict__)

class RandomGaussianUnitVector(Vector):
    def __init__(self, vector=None, dimensions=None, mu=None, sigma=None):
        if vector==None:
            vector = VectorGenerator.getRandomGaussianUnitVector(dimensions, mu, sigma)
            super(RandomGaussianUnitVector, self).__init__(vector.getNormalizedVector())
        else: super(RandomGaussianUnitVector, self).__init__(vector) 
    def getPermutedVector(self, permutation): return RandomGaussianUnitVector(dict([(k, self.getPermutedDimensionValue(permutation, k)) for k in self]))
    def getPermutedDimensionValue(self, permutation, dimension): return self[permutation.applyFunction(dimension)]
    def isPermutationSameAsVector(self, permutation): return range(self.dimension)==[permutation.applyFunction(i) for i in range(self.dimension)]
    

class VectorPermutation(Permutation):
    '''
    Generates permutations of vector.
    '''
    def __init__(self, dimensions): super(VectorPermutation, self).__init__(dimensions)
    @staticmethod
    def getPermutations(signatureLength, dimensions, randomGaussianUnitVector):
        vectorPermutations = []
        while len(vectorPermutations) < signatureLength:
            vectorPermutation = VectorPermutation(dimensions)
            if not randomGaussianUnitVector.isPermutationSameAsVector(vectorPermutation): 
                if vectorPermutation not in vectorPermutations: vectorPermutations.append(vectorPermutation)
        return vectorPermutations
    