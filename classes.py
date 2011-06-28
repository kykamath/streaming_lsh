'''
Created on Jun 14, 2011

@author: kykamath
'''
import random
from bitarray import bitarray
from Bio import trie
from library.vector import VectorGenerator, Vector
from library.math_modified import isPrime
from library.classes import TwoWayMap

class UtilityMethods:
    @staticmethod
    def updatePhraseTextAndDimensionsMap(phraseVector,  phraseTextAndDimensionMap, **settings):
        phraseIterator = phraseVector.iterkeys()
        while len(phraseTextAndDimensionMap)<settings['dimensions']:
            try:
                phrase = phraseIterator.next()
            except StopIteration: break
            if not phraseTextAndDimensionMap.contains(TwoWayMap.MAP_FORWARD, phrase): phraseId=len(phraseTextAndDimensionMap); phraseTextAndDimensionMap.set(TwoWayMap.MAP_FORWARD, phrase, phraseId)

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
        self.signatureTrie, self.isEmpty = trie.trie(), True
    def addDocument(self, document):
        permutedDocumentSignatureKey = document.signature.permutate(self).to01()
        if self.signatureTrie.has_key(permutedDocumentSignatureKey): self.signatureTrie[permutedDocumentSignatureKey].add(document.docId)
        else: self.signatureTrie[permutedDocumentSignatureKey] = set([document.docId])
        self.isEmpty=False
    def removeDocument(self, document):
        permutedDocumentSignatureKey = document.signature.permutate(self).to01()
        self.signatureTrie[permutedDocumentSignatureKey].remove(document.docId)
        if not self.signatureTrie[permutedDocumentSignatureKey]: del self.signatureTrie[permutedDocumentSignatureKey]
    def getNearestDocuments(self, document):
        if self.isEmpty: return set()
        permutedDocumentSignature = document.signature.permutate(self)
        nearestSignatureKey=SignatureTrie.getNearestSignatureKey(self.signatureTrie, permutedDocumentSignature)
        return self.signatureTrie[nearestSignatureKey]
        return set([1])
    def resetSignatureTrie(self): self.signatureTrie=trie.trie()
    
class Document(Vector):
    def __init__(self, docId, vector, clusterId = None):
        super(Document, self).__init__(vector)
        self.docId, self.clusterId = docId, clusterId
    def _getVectorMappedToDimension(self, vector, phraseTextAndDimensionMap): 
        mappedVector = Vector()
        phraseToDimensionMap = phraseTextAndDimensionMap.getMap(TwoWayMap.MAP_FORWARD)
        for phrase in self:
            if phrase in phraseToDimensionMap: mappedVector[phraseToDimensionMap[phrase]] = self[phrase]
        return mappedVector
    def setSignatureUsingVectors(self, vectors, phraseTextAndDimensionMap): 
        vectorMappedToDimension = self._getVectorMappedToDimension(vectors[0], phraseTextAndDimensionMap)
        self.signature = Signature(v.dotWithSmallerVectorWithSubsetDimensions(vectorMappedToDimension)>=0 for v in vectors)
    def setSignatureUsingVectorPermutations(self, vector, vectorPermutations, phraseTextAndDimensionMap):
        vectorMappedToDimension = self._getVectorMappedToDimension(vector, phraseTextAndDimensionMap)
        self.signature = Signature('')
        for vp in vectorPermutations:
            total = sum(vectorMappedToDimension[dimension]*vector[vp.applyFunction(dimension)] for dimension in vectorMappedToDimension)
            self.signature.append(total>=0)
    def __str__(self): return str(self.__dict__) + ' ' + str([s for s in self.iteritems()])

class RandomGaussianUnitVector(Vector):
    def __init__(self, vector=None, dimensions=None, mu=None, sigma=None):
        if vector==None:
            vector = VectorGenerator.getRandomGaussianUnitVector(dimensions, mu, sigma)
            super(RandomGaussianUnitVector, self).__init__(vector.getNormalizedVector())
        else: super(RandomGaussianUnitVector, self).__init__(vector) 
    def getPermutedVector(self, permutation): return RandomGaussianUnitVector(dict([(k, self.getPermutedDimensionValue(permutation, k)) for k in self]))
    def getPermutedDimensionValue(self, permutation, dimension): return self[permutation.applyFunction(dimension)]
    def isPermutationSameAsVector(self, permutation): return range(self.dimension)==[permutation.applyFunction(i) for i in range(self.dimension)]

class Cluster(Document):
    clusterIdCounter = 0
    ABOVE_THRESHOLD = 1
    BELOW_THRESHOLD = -1
    def __init__(self, vector):
        clusterId = 'cluster_%s'%Cluster.clusterIdCounter
        Cluster.clusterIdCounter+=1
        super(Cluster, self).__init__(clusterId, vector)
        self.clusterId, self.aggregateVector, self.vectorWeights = clusterId, vector, 1.
        self.documentsInCluster = {}
    def addDocument(self, document):
        self.aggregateVector+=document
        self.vectorWeights+=1
        for k in self.aggregateVector: self[k]=self.aggregateVector[k]/self.vectorWeights
        document.clusterId = self.clusterId
        self.documentsInCluster[document.docId] = document
    def iterateDocumentsInCluster(self): 
        documentsToDelete = []
        for doc in self.documentsInCluster: 
            if self.documentsInCluster[doc].clusterId == self.clusterId: yield self.documentsInCluster[doc]
            else: documentsToDelete.append(doc)
        for doc in documentsToDelete: del self.documentsInCluster[doc]
    @property
    def length(self): return len(list(self.iterateDocumentsInCluster()))
    @staticmethod
    def iterateByAttribute(clusters, attribute): 
        if attribute!='length':
            for cluster in clusters: yield (cluster, cluster.__dict__[attribute])
        else:
            for cluster in clusters: yield (cluster, cluster.length)
    @staticmethod
    def getClustersByAttributeAndThreshold(clusters, attribute, threshold, direction=1):
        if direction==Cluster.ABOVE_THRESHOLD:
            for cluster, value in Cluster.iterateByAttribute(clusters, attribute):
                if value>=threshold: yield cluster
        elif direction==Cluster.BELOW_THRESHOLD:
            for cluster, value in Cluster.iterateByAttribute(clusters, attribute):
                if value<threshold: yield cluster

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
