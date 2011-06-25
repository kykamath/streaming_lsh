'''
Created on Jun 25, 2011

@author: kykamath
'''
from classes import RandomGaussianUnitVector, VectorPermutation,\
    SignaturePermutation, Cluster
from operator import itemgetter

class StreamingLSHClustering:
    def __init__(self, **clustering_settings):
        self.thresholdForDocumentToBeInACluster = clustering_settings['threshold_for_document_to_be_in_cluster']
        self.unitVector = RandomGaussianUnitVector(dimensions=clustering_settings['dimensions'], mu=0, sigma=1)
        self.vectorPermutations = VectorPermutation.getPermutations(clustering_settings['signature_length'], clustering_settings['dimensions'], self.unitVector)
        self.signaturePermutations = [SignaturePermutation(clustering_settings['signature_length']) for i in range(clustering_settings['number_of_permutations'])]
        self.clusterMap = {}
    
    def getClusterForDocument(self, document):
        document.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations)
        predictedCluster = None
        possibleNearestClusters = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in self.signaturePermutations), set())
        if possibleNearestClusters: predictedCluster = max(((clusterId, self.clusterMap[clusterId].cosineSimilarity(document)) for clusterId in possibleNearestClusters), key=itemgetter(1))
        if predictedCluster and predictedCluster[1]>=self.thresholdForDocumentToBeInACluster:return predictedCluster[0]
    
    def getClusterAndUpdateExistingClusters(self, document):
        predictedCluster = self.getClusterForDocument(document)
        if predictedCluster!=None:
            self.clusterMap[predictedCluster].addDocument(document)
        else:
            newCluster = Cluster(document)
            newCluster.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations)
            for permutation in self.signaturePermutations: permutation.addDocument(newCluster)
            self.clusterMap[newCluster.clusterId] = newCluster
                