'''
Created on Jun 14, 2011

@author: kykamath
'''
import random
from bitarray import bitarray
from Bio import trie

class SignatureTrie:
    @staticmethod
    def getNearestSignatureKey(trie, signature):
        digitReplacement = {'0': '1', '1': '0'}
        targetKey, iteratingKey = signature.to01(), ''
        for i in range(len(targetKey)):
            iteratingKey+=targetKey[i]
            if not trie.has_prefix(iteratingKey): iteratingKey=iteratingKey[:-1]+digitReplacement[targetKey[i]]
        return iteratingKey

class Permutation:
    def __init__(self, signatureLength): 
        self.p, self.a, self.b = signatureLength, random.choice(range(signatureLength)[1::2]), random.choice(range(signatureLength))
        self.signatureTrie = trie.trie()
    def apply(self, x): return (self.a*x+self.b)%self.p
    def addDocument(self, document):
        permutedDocumentSignatureKey = document.signature.permutate(self).to01()
        if self.signatureTrie.has_key(permutedDocumentSignatureKey): self.signatureTrie[permutedDocumentSignatureKey].add(document.docId)
        else: self.signatureTrie[permutedDocumentSignatureKey] = set([document.docId])
    def getNearestDocuments(self, document):
        permutedDocumentSignature = document.signature.permutate(self)
        nearestSignatureKey=SignatureTrie.getNearestSignatureKey(self.signatureTrie, permutedDocumentSignature)
        return self.signatureTrie[nearestSignatureKey]
    def __str__(self): return 'p: %s, a: %s, b: %s'%(self.p, self.a, self.b)
    
class Signature(bitarray):
    def permutate(self, permutation): return Signature([self[permutation.apply(x)] for x in xrange(len(self))])
    
class Document:
    def __init__(self, docId, vector, clusterType = None): self.docId, self.vector, self.clusterType = docId, vector, clusterType
    def setDocumentSignatureUsingUnitRandomVectors(self, unitRandomVectors): 
        for rv in unitRandomVectors: self.signature = Signature(self.vector.dot(rv)>=0 for rv in unitRandomVectors)
    def __str__(self): return str(self.__dict__)
    
