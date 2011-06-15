'''
Created on Jun 14, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from Bio import trie
from classes import Signature, Permutation, SignatureTrie, Document
from library.vector import VectorGenerator

class SignatureTests(unittest.TestCase):
    def test_initialization(self):
        sgnt = Signature('1001011')
        self.assertEqual(sgnt.count(), 4)
        sgnt = Signature()
        self.assertEqual(sgnt.count(), 0)
    def test_permutate(self):
        sgnt = Signature('1001011')
        self.assertTrue(sgnt.count()==sgnt.permutate(Permutation(7)).count())
        
class SignatureTrieTests(unittest.TestCase):
    def setUp(self):
        self.tr = trie.trie()
        self.tr['1000']=12;self.tr['1011']=12; self.tr['1010']=12
        
    def test_getNearestSignature_exactKey(self): self.assertEquals(SignatureTrie.getNearestSignatureKey(self.tr, Signature('1000')), '1000')
    
    def test_getNearestSignature_nearbyKey(self): self.assertEquals(SignatureTrie.getNearestSignatureKey(self.tr, Signature('1100')), '1000')    
        
class PermutationTests(unittest.TestCase):
    def setUp(self):
        self.dimension, self.signatureLength = 500, 23
        self.unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1) for i in range(self.signatureLength)]
        
        self.doc1=Document(1, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        self.doc2=Document(2, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        self.doc1.setDocumentSignatureUsingUnitRandomVectors(self.unitRandomVectors); self.doc2.setDocumentSignatureUsingUnitRandomVectors(self.unitRandomVectors)
        
        self.pm = Permutation(signatureLength=self.signatureLength)
        self.pm.addDocument(self.doc1)
        self.pm.addDocument(self.doc2)
        
    def test_initialization(self):
        self.assertTrue(self.pm.a<self.pm.p and self.pm.b<self.pm.p)
        self.assertTrue(self.pm.a%2!=0)
        
    def test_permutationFunction(self):
        l = [self.pm.apply(i) for i in range(self.pm.p)]
        self.assertEqual(sorted(l), range(self.pm.p))
        
    def test_addDocument_newKey(self):
        doc1=Document(1, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        doc1.setDocumentSignatureUsingUnitRandomVectors(self.unitRandomVectors)
        pm = Permutation(signatureLength=self.signatureLength)
        pm.addDocument(doc1)
        self.assertEqual(pm.signatureTrie[doc1.signature.permutate(pm).to01()], set([1]))
        
    def test_addDocument_existingKey(self):
        newDocModifiedWithExistingSignature = Document(3, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        newDocModifiedWithExistingSignature.signature = Signature(self.doc1.signature.to01())
        self.pm.addDocument(newDocModifiedWithExistingSignature)
        self.assertEqual(self.pm.signatureTrie[self.doc1.signature.permutate(self.pm).to01()], set([1, 3]))
        
    def test_getNearestDocument_usingAKeyAlreadyInTrie(self): self.assertEqual(self.pm.getNearestDocuments(self.doc1), set([1]))
    
    def test_getNearestDocument_usingANearbyKeyInTrie(self):
        digitReplacement = {'0': '1', '1': '0'}
        newDocWithANearbySignature = Document(3, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        exactSignature = self.doc1.signature.to01() 
        newDocWithANearbySignature.signature = Signature(exactSignature[:-1]+digitReplacement[exactSignature[-1]])
        self.assertNotEquals(self.doc1.signature.to01(), newDocWithANearbySignature.signature.to01())
        # Next assertion can sometimes fail because of randomization.
        self.assertEqual(self.pm.getNearestDocuments(newDocWithANearbySignature), set([1]))
        
if __name__ == '__main__':
    unittest.main()