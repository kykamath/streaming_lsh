'''
Created on Jun 14, 2011

@author: kykamath
'''
import random
from bitarray import bitarray
from Bio import trie
from library.vector import VectorGenerator
from library.math_modified import isPrime

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
    def permutate(self, permutation): return Signature([self[permutation.apply(x)] for x in xrange(len(self))])

class Permutation(object):
    def __init__(self, maximumValue): 
        if not isPrime(maximumValue): raise Exception('Maximum value should be prime')
        self.p, self.a, self.b = maximumValue, random.choice(range(maximumValue)[1::2]), random.choice(range(maximumValue))
    def apply(self, x): return (self.a*x+self.b)%self.p
    
class SignaturePermutation(Permutation):
    def __init__(self, signatureLength): 
#        self.p, self.a, self.b = signatureLength, random.choice(range(signatureLength)[1::2]), random.choice(range(signatureLength))
        super(SignaturePermutation, self).__init__(signatureLength)
        self.signatureTrie = trie.trie()
#    def apply(self, x): return (self.a*x+self.b)%self.p
    def addDocument(self, document):
        permutedDocumentSignatureKey = document.signature.permutate(self).to01()
        if self.signatureTrie.has_key(permutedDocumentSignatureKey): self.signatureTrie[permutedDocumentSignatureKey].add(document.docId)
        else: self.signatureTrie[permutedDocumentSignatureKey] = set([document.docId])
    def getNearestDocuments(self, document):
        permutedDocumentSignature = document.signature.permutate(self)
        nearestSignatureKey=SignatureTrie.getNearestSignatureKey(self.signatureTrie, permutedDocumentSignature)
        return self.signatureTrie[nearestSignatureKey]
    def __str__(self): return 'p: %s, a: %s, b: %s'%(self.p, self.a, self.b)
    
class Document:
    def __init__(self, docId, vector, clusterType = None): self.docId, self.vector, self.clusterType = docId, vector, clusterType
    def setDocumentSignatureUsingUnitRandomVectors(self, unitRandomVectors): 
        for rv in unitRandomVectors: self.signature = Signature(self.vector.dot(rv)>=0 for rv in unitRandomVectors)
    def __str__(self): return str(self.__dict__)

class RandomGaussianUnitVector():
    def __init__(self, dimensions, mu, sigma):
        vector = VectorGenerator.getRandomGaussianUnitVector(dimensions, mu, sigma)
        self.vector = vector.getNormalizedVector()
#    def permutate(self, permutation): return 

class RandomGaussianUnitVectorPermutation(Permutation):
    def __init__(self, dimensions): super(RandomGaussianUnitVectorPermutation, self).__init__(dimensions)
    
     
    