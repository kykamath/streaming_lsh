'''
Created on Jun 14, 2011

@author: kykamath
'''
import unittest
from Bio import trie
from classes import Signature, Permutation, SignatureTrie

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
        self.pm = Permutation(13)
    def test_initialization(self):
        self.assertTrue(self.pm.a<self.pm.p and self.pm.b<self.pm.p)
        self.assertTrue(self.pm.a%2!=0)
    def test_permutationFunction(self):
        l = [self.pm.apply(i) for i in range(self.pm.p)]
        self.assertEqual(sorted(l), range(self.pm.p))
    def test_addDocument_newKey(self):
        pass
    def test_addDocument_existingKey(self):
        pass
    def test_removeDocument(self):
        pass
    def test_getNearestDocument_existingKey(self):
        pass
    def test_getNearestDocument_nearestKey(self):
        pass
    def test_getNearestDocument_multipleDocumentsReturned(self):
        pass
        
if __name__ == '__main__':
    unittest.main()