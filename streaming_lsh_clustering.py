'''
Created on Jun 25, 2011

@author: kykamath
'''
from classes import RandomGaussianUnitVector, VectorPermutation,\
    SignaturePermutation, Cluster, UtilityMethods
from operator import itemgetter
from library.classes import TwoWayMap

class StreamingLSHClustering(object):
    def __init__(self, **clustering_settings):
        self.thresholdForDocumentToBeInACluster = clustering_settings['threshold_for_document_to_be_in_cluster']
        self.unitVector = RandomGaussianUnitVector(dimensions=clustering_settings['dimensions'], mu=0, sigma=1)
        self.vectorPermutations = VectorPermutation.getPermutations(clustering_settings['signature_length'], clustering_settings['dimensions'], self.unitVector)
        self.signaturePermutations = [SignaturePermutation(clustering_settings['signature_length']) for i in range(clustering_settings['number_of_permutations'])]
        self.phraseTextAndDimensionMap, self.clusters = TwoWayMap(), {}
        self.clustering_settings = clustering_settings
    
    def getClusterForDocument(self, document):
        UtilityMethods.updatePhraseTextAndDimensionsMap(document, self.phraseTextAndDimensionMap, **self.clustering_settings)
        document.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)
        predictedCluster = None
        possibleNearestClusters = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in self.signaturePermutations), set())
#        if possibleNearestClusters: predictedCluster = max(((clusterId, self.clusters[clusterId].cosineSimilarity(document)) for clusterId in possibleNearestClusters), key=itemgetter(1))
#        if predictedCluster and predictedCluster[1]>=self.thresholdForDocumentToBeInACluster:return predictedCluster[0]
    
    def getClusterAndUpdateExistingClusters(self, document):
        predictedCluster = self.getClusterForDocument(document)
        if predictedCluster!=None:
            self.clusters[predictedCluster].addDocument(document)
        else:
            newCluster = Cluster(document)
            newCluster.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)
            for permutation in self.signaturePermutations: permutation.addDocument(newCluster)
            self.clusters[newCluster.clusterId] = newCluster
    
    def regenerateSignatureForClusters(self):
        for cluster in self.clusters.itervalues(): cluster.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)

if __name__ == '__main__':
    s = set([1,3,3])
    s2=set([4,5])
    
    a=list()
    a+=s
    a+=s2
#    print reduce(lambda x,y: x.union(y), [s,s2], set())
    print a