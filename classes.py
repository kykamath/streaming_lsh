'''
Created on Jun 14, 2011

@author: kykamath
'''
from bitarray import bitarray
import random

class Permutation:
    def __init__(self, signatureLength): 
        self.p, self.a, self.b = signatureLength, random.choice(range(signatureLength)[1::2]), random.choice(range(signatureLength))
        self.documentSignatures = {}
    def apply(self, x): return (self.a*x+self.b)%self.p
    def __str__(self): return 'p: %s, a: %s, b: %s'%(self.p, self.a, self.b)
    
class Signature(bitarray):
    def permutate(self, permutation): return Signature([self[permutation.apply(x)] for x in xrange(len(self))])
    @staticmethod
    def sorted(signatures): 
        print sorted(signatures)
        
class Document:
    def __init__(self, docId, vector): self.docId, self.vector = docId, vector
    def initializeSignatureForVector(self, unitRandomVectors): self.signature = Signature(self.vector.dot(rv)>=0 for rv in unitRandomVectors)
    def __str__(self): return str(self.vector)
    
if __name__ == '__main__':
    print dict((i, 'a') for i in xrange(4))