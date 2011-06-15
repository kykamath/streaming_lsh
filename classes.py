'''
Created on Jun 14, 2011

@author: kykamath
'''
from bitarray import bitarray
import random

class Permutation:
    def __init__(self, signatureLength): self.p, self.a, self.b = signatureLength, random.choice(range(signatureLength)[1::2]), random.choice(range(signatureLength))
    def apply(self, x): return (self.a*x+self.b)%self.p
    def __str__(self): return 'p: %s, a: %s, b: %s'%(self.p, self.a, self.b)
    
class Signature(bitarray):
    def permutate(self, permutation): return Signature([self[permutation.apply(x)] for x in xrange(len(self))])
        
class Document:
    def __init__(self, vector): self.vector = vector
    def initializeSignatureForVector(self, unitRandomVectors): self.signature = Signature(self.vector.dot(rv)>=0 for rv in unitRandomVectors)
    def __str__(self): return str(self.vector)