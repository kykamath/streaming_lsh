'''
A demo for clustering text document using locality sensitive hashing.

Command to run the demo: python StreamingLSHClusteringDemo.py

The input document used in this demo is in the following format:
<cluster_id> <document>
Example:
1 abc def efe tert ertre
2 sdf ertr frf frfe
1 sdfds sdfdsf dsfewf

Created on Jun 16, 2011

@author: kykamath
'''
import sys, numpy
sys.path.append('../')
from streaming_lsh_clustering import StreamingLSHClustering
from library.file_io import FileIO 
from classes import Document
from library.vector import Vector
from library.clustering import EvaluationMetrics

def createDocumentFromLine(docId, line):
    vector, words = Vector(), line.split()
    for word in words[1:]:
        if word not in vector: vector[word]=1
        else: vector[word]+=1
    return Document(docId, vector, clusterId=words[0])


def streamingLSHClusteringDemo():
    clustering_settings = {'dimensions': 53,
                            'signature_length': 13,
                            'number_of_permutations': 5,
                            'threshold_for_document_to_be_in_cluster': 0.2}
    clustering=StreamingLSHClustering(**clustering_settings)
    docId = 0
    docsToOriginalClusterMap = {}
    for line in FileIO.iterateLinesFromFile('../data/streaming.dat'):
        document = createDocumentFromLine(docId, line)
        docsToOriginalClusterMap[docId] = document.clusterId
        docId+=1
        clustering.getClusterAndUpdateExistingClusters(document)
    clusterLabels = []
    for k, cluster in clustering.clusters.iteritems(): clusterLabels.append([docsToOriginalClusterMap[doc.docId] for doc in cluster.iterateDocumentsInCluster()])
    return EvaluationMetrics.getValueForClusters(clusterLabels, EvaluationMetrics.purity)
        
if __name__ == '__main__':
    print numpy.mean([streamingLSHClusteringDemo() for i in range(10)])
