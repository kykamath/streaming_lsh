'''
Created on Jun 14, 2011

@author: kykamath
'''
import sys, math, unittest
sys.path.append('../')
from Bio import trie
from classes import Signature, SignaturePermutation, SignatureTrie, Document,\
    RandomGaussianUnitVector, Permutation, VectorPermutation
from library.vector import VectorGenerator
import library.math_modified as math_mod

class SignatureTests(unittest.TestCase):
    def test_initialization(self):
        sgnt = Signature('1001011')
        self.assertEqual(sgnt.count(), 4)
        sgnt = Signature()
        self.assertEqual(sgnt.count(), 0)
    def test_permutate(self):
        sgnt = Signature('1001011')
        self.assertTrue(sgnt.count()==sgnt.permutate(SignaturePermutation(7)).count())
        
class SignatureTrieTests(unittest.TestCase):
    def setUp(self):
        self.tr = trie.trie()
        self.tr['1000']=12;self.tr['1011']=12; self.tr['1010']=12
        
    def test_getNearestSignature_exactKey(self): self.assertEquals(SignatureTrie.getNearestSignatureKey(self.tr, Signature('1000')), '1000')
    
    def test_getNearestSignature_nearbyKey(self): self.assertEquals(SignatureTrie.getNearestSignatureKey(self.tr, Signature('1100')), '1000')    
        

class PermutationTests(unittest.TestCase):
    def setUp(self): self.pm = Permutation(maximumValue=13)
    def test_exceptionForMaxValueNotPrime(self): self.assertRaises(Exception, Permutation, 10)
    def test_initialization(self):
        self.assertTrue(self.pm.a<self.pm.p and self.pm.b<self.pm.p)
        self.assertTrue(self.pm.a%2!=0)
    def test_applyFunction(self):
        l = [self.pm.applyFunction(i) for i in range(self.pm.p)]
        self.assertEqual(sorted(l), range(self.pm.p))
    def test_applyInverseFunction(self):
        l = [self.pm.applyFunction(i) for i in range(self.pm.p)]
        print self.pm
        print 'x', range(self.pm.p)
        print 'y', l
        print math_mod.gcd(self.pm.a,self.pm.p)
#        N = [(self.pm.a*x+self.pm.b-y)/self.pm.p for x,y in zip(range(self.pm.p), l)]
#        print N
#        print [(y-self.pm.b-n*self.pm.p)/self.pm.a for y,n in zip(l,N)]
#        self.assertEqual(range(self.pm.p), [self.pm.applyInverseFunction(i) for i in l])
    def test_equality(self):
        pm1 = Permutation(maximumValue=13)
        pm1.a=self.pm.a;pm1.b=self.pm.b
        self.assertEqual(pm1, self.pm)
        self.assertTrue(pm1 in [self.pm])
        
class DocumentTests(unittest.TestCase):
    def test_setSignatureUsingVectorPermutations(self): 
        dimensions, signatureLength = 53, 13
        unitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        vectorPermutations = VectorPermutation.getPermutations(signatureLength, dimensions, unitVector)
        permutatedUnitVectors = [unitVector.getPermutedVector(r) for r in vectorPermutations]
        
        documentVector = VectorGenerator.getRandomGaussianUnitVector(dimension=dimensions, mu=0, sigma=1)
        documentWithSignatureByVectors=Document(1, documentVector)
        documentWithSignatureByVectorPermutations=Document(2, documentVector)
        
        documentWithSignatureByVectors.setSignatureUsingVectors(permutatedUnitVectors)
        print documentWithSignatureByVectors.signature
        documentWithSignatureByVectorPermutations.setSignatureUsingVectorPermutations(unitVector, vectorPermutations)
#        self.assertEqual(documentWithSignatureByVectors.signature, documentWithSignatureByVectorPermutations.signature)
        
class SignaturePermutationTests(unittest.TestCase):
    def setUp(self):
        self.dimension, self.signatureLength = 50, 23
        self.unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1) for i in range(self.signatureLength)]
        
        self.doc1=Document(1, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        self.doc2=Document(2, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        self.doc1.setSignatureUsingVectors(self.unitRandomVectors); self.doc2.setSignatureUsingVectors(self.unitRandomVectors)
        
        self.pm = SignaturePermutation(signatureLength=self.signatureLength)
        self.pm.addDocument(self.doc1)
        self.pm.addDocument(self.doc2)
        
    def test_addDocument_newKey(self):
        doc1=Document(1, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        doc1.setSignatureUsingVectors(self.unitRandomVectors)
        pm = SignaturePermutation(signatureLength=self.signatureLength)
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

class RandomGaussianUnitVectorTests(unittest.TestCase):
    def setUp(self): 
        self.vector = RandomGaussianUnitVector(dimensions=5, mu=0, sigma=1)
        self.permutation = VectorPermutation(dimensions=5)
    def test_initialization(self): self.assertEquals('%0.0f'%self.vector.mod(),'1')
    def test_getPermutedDimensionValue(self): self.assertEqual(self.vector[self.permutation.applyFunction(10)], self.vector.getPermutedDimensionValue(self.permutation, 10))
    def test_getPermutedVector(self): 
        permutedVector = self.vector.getPermutedVector(self.permutation)
        self.assertEqual(RandomGaussianUnitVector, type(permutedVector))
        self.assertNotEqual(self.vector, permutedVector)
        self.assertEqual('1', '%0.0f'%permutedVector.mod())
    def test_isPermutationSameAsVector(self):
        self.permutation.a=1
        self.permutation.b=0
        self.assertTrue(self.vector.isPermutationSameAsVector(self.permutation))

class VectorPermutationTests(unittest.TestCase):
    def setUp(self): self.pm = VectorPermutation(dimensions=13)
    def test_exceptionForMaxValueNotPrime(self): self.assertRaises(Exception, Permutation, 10)
    def test_initialization(self):
        self.assertTrue(self.pm.a<self.pm.p and self.pm.b<self.pm.p)
        self.assertTrue(self.pm.a%2!=0)
        self.assertTrue(0==self.pm.b)
    def test_applyFunction(self):
#        print self.pm
        l = [self.pm.applyFunction(i) for i in range(self.pm.p)]
        self.assertEqual(sorted(l), range(self.pm.p))
#        print range(self.pm.p)
#        print l

if __name__ == '__main__':
    unittest.main()