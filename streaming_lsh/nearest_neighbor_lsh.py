'''
Created on Sep 16, 2011

@author: kykamath
'''
from classes import RandomGaussianUnitVector, VectorPermutation,\
    SignaturePermutationWithTrie, UtilityMethods, Document
from operator import itemgetter
from library.classes import TwoWayMap

class NearestNeighborUsingLSH(object):
    def __init__(self, **settings):
        self.settings = settings
        self.nearestNeighborThreshold = settings['nearest_neighbor_threshold']
        self.unitVector = RandomGaussianUnitVector(dimensions=settings['dimensions'], mu=0, sigma=1)
        self.vectorPermutations = VectorPermutation.getPermutations(settings['signature_length'], settings['dimensions'], self.unitVector)
        self.signaturePermutations = [SignaturePermutationWithTrie(settings['signature_length']) for i in range(settings['number_of_permutations'])]
        self.phraseTextAndDimensionMap = TwoWayMap()
        self.documentIdToDocumentMap = {}
    
    def update(self, newDocument):
        UtilityMethods.updatePhraseTextAndDimensionsMap(newDocument, self.phraseTextAndDimensionMap, **self.settings)
        currentDocument = self.documentIdToDocumentMap.get(newDocument.docId, None)
        self.documentIdToDocumentMap[newDocument.docId] = newDocument
        newDocument.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)
        for permutation in self.signaturePermutations: 
            if currentDocument!=None: permutation.removeDocument(currentDocument)
            permutation.addDocument(newDocument)
        
    def getNearestDocument(self, document):
        UtilityMethods.updatePhraseTextAndDimensionsMap(document, self.phraseTextAndDimensionMap, **self.settings)
        document.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)
        predictedNeighbor = None
        possibleNearestNeighbors = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in self.signaturePermutations), set())
        if possibleNearestNeighbors: predictedNeighbor = max(((docId, document.cosineSimilarity(document)) for docId in possibleNearestNeighbors), key=itemgetter(1))
        if predictedNeighbor and predictedNeighbor[1]>=self.nearestNeighborThreshold:return predictedNeighbor[0]    