'''
Created on Jun 14, 2011

@author: kykamath
'''
import sys, unittest
sys.path.append('../')
from Bio import trie
from library.classes import TwoWayMap
from classes import Signature, SignaturePermutation, SignatureTrie, Document,\
    RandomGaussianUnitVector, Permutation, VectorPermutation, Cluster,\
    UtilityMethods
from library.vector import VectorGenerator, Vector

settings = {}

class UtilityMethodsTests(unittest.TestCase):
    def setUp(self):
        self.phraseVector = {'project':1, 'cluster':1, 'highdimensional':1, 'streams':1}
        self.phraseTextAndDimensionMap = TwoWayMap()
        self.phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, 'project', 0)
        self.phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, 'cluster', 1)
        self.finalPhraseToIdMap = {'project': 0, 'cluster': 1, 'streams': 2, 'highdimensional': 3}
        settings['dimensions'] = 2
    def test_updatePhraseTextAndDimensionsMap_PhraseMapHasLesserDimensions(self):
        settings['dimensions'] = 4
        UtilityMethods.updatePhraseTextAndDimensionsMap(self.phraseVector, self.phraseTextAndDimensionMap, **settings)
        self.assertEqual(self.finalPhraseToIdMap, self.phraseTextAndDimensionMap.getMap(TwoWayMap.MAP_FORWARD))
    def test_updatePhraseTextAndDimensionsMap_PhraseMapHasMaximumDimensions(self):
        UtilityMethods.updatePhraseTextAndDimensionsMap(self.phraseVector, self.phraseTextAndDimensionMap, **settings)
        for k in ['streams', 'highdimensional']: del self.finalPhraseToIdMap[k]
        self.assertEqual(self.finalPhraseToIdMap, self.phraseTextAndDimensionMap.getMap(TwoWayMap.MAP_FORWARD))
    
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
    def test_equality(self):
        pm1 = Permutation(maximumValue=13)
        pm1.a=self.pm.a;pm1.b=self.pm.b
        self.assertEqual(pm1, self.pm)
        self.assertTrue(pm1 in [self.pm])
        
class DocumentTests(unittest.TestCase):
    def test_setSignatureUsingVectorPermutations(self): 
        dimensions, signatureLength = 53, 13
        phraseTextAndDimensionMap = TwoWayMap()
        for i in range(dimensions): phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, i,i)
        phraseTextAndDimensionMapWithMissingDimensions = TwoWayMap()
        for i in range(dimensions-50): phraseTextAndDimensionMapWithMissingDimensions.set(TwoWayMap.MAP_FORWARD, i,i)
        
        unitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        vectorPermutations = VectorPermutation.getPermutations(signatureLength, dimensions, unitVector)
        permutatedUnitVectors = [unitVector.getPermutedVector(r) for r in vectorPermutations]
        documentVector = VectorGenerator.getRandomGaussianUnitVector(dimension=dimensions, mu=0, sigma=1)
        documentWithSignatureByVectors=Document(1, documentVector)
        documentWithSignatureByVectorPermutations=Document(2, documentVector)
        documentWithSignatureByVectors.setSignatureUsingVectors(permutatedUnitVectors, phraseTextAndDimensionMap)
        documentWithSignatureByVectorPermutations.setSignatureUsingVectorPermutations(unitVector, vectorPermutations, phraseTextAndDimensionMap)
        self.assertEqual(documentWithSignatureByVectors.signature, documentWithSignatureByVectorPermutations.signature)
        documentWithSignatureByVectors.setSignatureUsingVectors(permutatedUnitVectors, phraseTextAndDimensionMapWithMissingDimensions)
        documentWithSignatureByVectorPermutations.setSignatureUsingVectorPermutations(unitVector, vectorPermutations, phraseTextAndDimensionMapWithMissingDimensions)
        self.assertEqual(documentWithSignatureByVectors.signature, documentWithSignatureByVectorPermutations.signature)

    def test_setSignatureUsingVectors(self):
        phraseTextAndDimensionMap = TwoWayMap()
        phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, 'a', 1)
        phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, 'b', 2)
        documentWithDimensionsInVector = Document(1, {'a':1, 'b':4})
        documentWithDimensionsNotInVector = Document(1, {'a':1, 'c':4})
        vectors = [ Vector({1: 3/5., 2: -4/5.}), Vector({1:-5/13., 2: 12/13.})]
        documentWithDimensionsInVector.setSignatureUsingVectors(vectors, phraseTextAndDimensionMap)
        documentWithDimensionsNotInVector.setSignatureUsingVectors(vectors, phraseTextAndDimensionMap)
        self.assertEqual(Signature('01'), documentWithDimensionsInVector.signature)
        self.assertEqual(Signature('10'), documentWithDimensionsNotInVector.signature)
        
        
class SignaturePermutationTests(unittest.TestCase):
    def setUp(self):
        self.dimension, self.signatureLength = 50, 23
        self.phraseTextAndDimensionMap = TwoWayMap()
        for i in range(self.dimension): self.phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, i,i)
        self.unitRandomVectors = [VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1) for i in range(self.signatureLength)]
        self.doc1=Document(1, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        self.doc2=Document(2, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        self.doc1.setSignatureUsingVectors(self.unitRandomVectors, self.phraseTextAndDimensionMap); self.doc2.setSignatureUsingVectors(self.unitRandomVectors, self.phraseTextAndDimensionMap)
        self.pm = SignaturePermutation(signatureLength=self.signatureLength)
        self.pm.addDocument(self.doc1)
        self.pm.addDocument(self.doc2)
    def test_addDocument_newKey(self):
        doc1=Document(1, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        doc1.setSignatureUsingVectors(self.unitRandomVectors, self.phraseTextAndDimensionMap)
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
        self.assertEqual(self.pm.getNearestDocuments(newDocWithANearbySignature), set([1])) # This assertion can sometimes fail because of randomization. Run the tests again. It's OK!
    def test_getNearestDocument_emptyTrie(self):
        permutationWithEmptyTrie = SignaturePermutation(signatureLength=self.signatureLength)
        self.assertEqual(permutationWithEmptyTrie.getNearestDocuments(self.doc1), set())
    def test_removeDocument_documents(self):
        newDocModifiedWithExistingSignature = Document(3, VectorGenerator.getRandomGaussianUnitVector(dimension=self.dimension, mu=0, sigma=1))
        newDocModifiedWithExistingSignature.signature = Signature(self.doc1.signature.to01())
        self.pm.addDocument(newDocModifiedWithExistingSignature)
        self.assertEqual(self.pm.signatureTrie[self.doc1.signature.permutate(self.pm).to01()], set([1, 3]))
        self.pm.removeDocument(newDocModifiedWithExistingSignature)
        self.assertEqual(self.pm.signatureTrie[self.doc1.signature.permutate(self.pm).to01()], set([1]))
        self.pm.removeDocument(self.doc1)
        self.assertEqual(None, self.pm.signatureTrie.get(self.doc1.signature.permutate(self.pm).to01()))
    def test_resetSignatureTrie(self):
        self.assertTrue(len(self.pm.signatureTrie)>0)
        self.pm.resetSignatureTrie()
        self.assertTrue(len(self.pm.signatureTrie)==0)
        
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

class ClusterTests(unittest.TestCase):
    def setUp(self): 
        Cluster.clusterIdCounter = 0
        self.docx = Document(1, {1:2,2:4})
        self.docy = Document(2, {2:4})
        self.cluster1 = Cluster(self.docx)
        self.cluster2 = Cluster(self.docy)
        self.doc1 = Document(3, Vector({3:4}))
        self.doc2 = Document(4, Vector({2:4}))
    def test_initialization(self):
        self.assertEqual('cluster_0', self.cluster1.clusterId)
        self.assertEqual('cluster_1', self.cluster2.clusterId)
        self.assertEqual(2, Cluster.clusterIdCounter)
        self.assertEqual([self.docx], list(self.cluster1.iterateDocumentsInCluster()))
        self.assertEqual([self.docy], list(self.cluster2.iterateDocumentsInCluster()))
    def test_addDocument(self):
        self.cluster1.addDocument(self.doc1)
        # Test if cluster id is set.
        self.assertEqual(self.cluster1.clusterId, self.doc1.clusterId)
        # Test that cluster mean is updated.
        self.assertEqual({1:2/2.,2:2.,3:2.}, self.cluster1)
        # Test that cluster aggrefate is updated.
        self.assertEqual({1:2,2:4,3:4}, self.cluster1.aggregateVector)
        # Test that document is added to cluster documents.
        self.assertEqual(self.doc1, self.cluster1.documentsInCluster[self.doc1.docId])
        self.cluster1.addDocument(self.doc2)
        self.assertEqual(3, self.cluster1.vectorWeights)
        self.assertEqual({1:2/3.,2:8/3.,3:4/3.}, self.cluster1)
        self.assertEqual({1:2,2:8,3:4}, self.cluster1.aggregateVector)
    def test_iterateDocumentsInCluster(self):
        # Test normal iteration.
        self.cluster1.addDocument(self.doc1)
        self.cluster1.addDocument(self.doc2)
        self.assertEqual([self.docx, self.doc1, self.doc2], list(self.cluster1.iterateDocumentsInCluster()))
        self.assertEqual(3, self.cluster1.length)
        # Test removal of document from cluster, if the document is added to a different cluster.
        self.cluster2.addDocument(self.doc2)
        self.assertEqual([self.docx, self.doc1], list(self.cluster1.iterateDocumentsInCluster()))
        self.assertEqual(2, self.cluster1.length)
        self.assertEqual(2, len(self.cluster1.documentsInCluster))
        self.assertEqual([self.docy, self.doc2], list(self.cluster2.iterateDocumentsInCluster()))
        self.assertEqual(2, self.cluster2.length)
    def test_iterateByAttribute(self):
        self.cluster1.addDocument(self.doc1)
        self.cluster2.addDocument(self.doc2)
        self.assertEqual([(self.cluster1, 'cluster_0'), (self.cluster2, 'cluster_1')], list(Cluster.iterateByAttribute([self.cluster1, self.cluster2], 'clusterId')))
    def test_filterClustersByAttribute(self):
        self.cluster1.addDocument(self.doc1)
        self.cluster2.addDocument(self.doc2)
        self.assertEqual([self.cluster1, self.cluster2], list(Cluster.getClustersByAttributeAndThreshold([self.cluster1, self.cluster2], 'vectorWeights', 1)))
        self.assertEqual([], list(Cluster.getClustersByAttributeAndThreshold([self.cluster1, self.cluster2], 'vectorWeights', 3)))
        self.assertEqual([self.cluster1, self.cluster2], list(Cluster.getClustersByAttributeAndThreshold([self.cluster1, self.cluster2], 'vectorWeights', 3, Cluster.BELOW_THRESHOLD)))

if __name__ == '__main__':
    unittest.main()
    