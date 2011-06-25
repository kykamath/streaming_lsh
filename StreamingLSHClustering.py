'''
Created on Jun 25, 2011

@author: kykamath
'''
from classes import RandomGaussianUnitVector, VectorPermutation,\
    SignaturePermutation, Cluster
from operator import itemgetter

class StreamingLSHClustering:
    def __init__(self, documentIterator, **clustering_settings):
        dimensions = clustering_settings['dimensions']
        signatureLength=clustering_settings['signature_length']
        numberOfPermutations = clustering_settings['number_of_permutations']
        thresholdForDocumentToBeInACluster = clustering_settings['threshold_for_document_to_be_in_cluster']
        
        unitVector = RandomGaussianUnitVector(dimensions=dimensions, mu=0, sigma=1)
        vectorPermutations = VectorPermutation.getPermutations(signatureLength, dimensions, unitVector)
        signaturePermutations = [SignaturePermutation(signatureLength) for i in range(numberOfPermutations)]
        
        # Process the stream.
#        docId = 0
#        docsToOriginalClusterMap = {}
        clusterMap = {}
        for document in documentIterator:
#            docsToOriginalClusterMap[docId] = document.clusterId
#            docId+=1
            document.setSignatureUsingVectorPermutations(unitVector, vectorPermutations)
            # Get nearest cluster is different permutations
            # If nearest clusters exist AND above threshold,
            #    Update the neigbours mean with the document
            #    Mark the document to belong to a cluster id
            # If no neighbors,
            #    Create a new cluster. Add the document as new cluster
            #    Add the cluster to all permutations.
            predictedCluster = None
            possibleNearestClusters = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in signaturePermutations), set())
            if possibleNearestClusters: predictedCluster = max(((clusterId, clusterMap[clusterId].cosineSimilarity(document)) for clusterId in possibleNearestClusters), key=itemgetter(1))
            if predictedCluster and predictedCluster[1]>=thresholdForDocumentToBeInACluster:
                clusterMap[predictedCluster[0]].addDocument(document)
            else:
                newCluster = Cluster(document)
                newCluster.setSignatureUsingVectorPermutations(unitVector, vectorPermutations)
                for permutation in signaturePermutations: permutation.addDocument(newCluster)
                clusterMap[newCluster.clusterId] = newCluster
