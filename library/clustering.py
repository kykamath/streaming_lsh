'''
Created on Jun 15, 2011

@author: kykamath
'''

import cjson, math
from numpy import *
from scipy.stats import mode
from nltk import cluster
import random
from collections import defaultdict
from operator import itemgetter
from classes import TwoWayMap
from vector import VectorGenerator

class EvaluationMetrics:
    '''
    The implementation for many of these metrics was obtained at
    http://blog.sun.tc/2010/11/clustering-evaluation-for-numpy-and-scipy.html.
    The original authors email id is lin.sun84@gmail.com.
    '''
    @staticmethod
    def precision(predicted,labels):
        K=unique(predicted)
        p=0
        for cls in K:
            cls_members=nonzero(predicted==cls)[0]
            if cls_members.shape[0]<=1:
                continue
            real_label=mode(labels[cls_members])[0][0]
            correctCount=nonzero(labels[cls_members]==real_label)[0].shape[0]
            p+=double(correctCount)/cls_members.shape[0]
        return p/K.shape[0]
 
    @staticmethod
    def recall(predicted,labels):
        K=unique(predicted)
        ccount=0
        for cls in K:
            cls_members=nonzero(predicted==cls)[0]
            real_label=mode(labels[cls_members])[0][0]
            ccount+=nonzero(labels[cls_members]==real_label)[0].shape[0]
        return double(ccount)/predicted.shape[0] 
    
    @staticmethod
    def f1(predicted,labels):
        p=EvaluationMetrics.precision(predicted,labels)
        r=EvaluationMetrics.recall(predicted,labels)
        return 2*p*r/(p+r),p,r
    
    @staticmethod
    def purity(predicted,labels):
        correctAssignedItems = 0.0
        for u,v in zip(predicted,labels):
            if u==v: correctAssignedItems+=1
        return correctAssignedItems/len(predicted) 

    @staticmethod
    def _getPredictedAndLabels(clusters):
        labels=[]
        predicted=clusters
        for cluster in clusters:
            classBySize = defaultdict(int)
            for item in cluster: classBySize[item]+=1
            clusterType = sorted(classBySize.iteritems(),key=itemgetter(1), reverse=True)[0][0]
            labels.append([clusterType]*len(cluster))
        p,l=[],[]
        for pre in predicted: p+=pre
        for lab in labels: l+=lab
        return (array(p), array(l))

    @staticmethod
    def getValueForClusters(predicted, evaluationMethod):
        predictedModified = [p for p in predicted if p]
        if predictedModified:
            predicted, labels = EvaluationMetrics._getPredictedAndLabels(predictedModified)
            return evaluationMethod(predicted, labels)
        else: return 0

class TrainingAndTestDocuments:
    @staticmethod
    def generate(numberOfDocuments = 2500, dimensions = 52):
        def pickOneByProbability(objects, probabilities):
            initialValue, objectToRange = 0.0, {}
            for i in range(len(objects)):
                objectToRange[objects[i]]=(initialValue, initialValue+probabilities[i])
                initialValue+=probabilities[i]
            randomNumber = random.random()
            for object, rangeVal in objectToRange.iteritems():
                if rangeVal[0]<=randomNumber<=rangeVal[1]: return object
                
        topics = {
                  'elections':{'prob': 0.3, 'tags': {'#gop': 0.4, '#bachmann': 0.2, '#perry': 0.2, '#romney': 0.2}},
                  'soccer': {'prob': 0.2, 'tags': {'#rooney': 0.15, '#chica': 0.1, '#manutd': 0.6, '#fergie': 0.15}},
                  'arab': {'prob': 0.3, 'tags': {'#libya': 0.4, '#arab': 0.3, '#eqypt': 0.15, '#syria': 0.15}},
                  'page3': {'prob': 0.2, 'tags': {'#paris': 0.2, '#kim': 0.4, '#britney': 0.2, '#khloe': 0.2}},
                  }
        stopwords = 'abcdefghijklmnopqrstuvwxyz1234567890'
        
        print '#', cjson.encode({'dimensions': dimensions})
        for i in range(numberOfDocuments):
            topic = pickOneByProbability(topics.keys(), [topics[k]['prob'] for k in topics.keys()])
            print ' '.join([topic] + [pickOneByProbability(topics[topic]['tags'].keys(), [topics[topic]['tags'][k] for k in topics[topic]['tags'].keys()]) for i in range(2)] + [random.choice(stopwords) for i in range(5)])

class EMTextClustering:
    '''
    Clusters documents given in the form 
    [(id, text), (id, text), ...., (id, text)]
    '''
    PHRASE_TO_DIMENSION = TwoWayMap.MAP_FORWARD
    DIMENSION_TO_PHRASE = TwoWayMap.MAP_REVERSE
    def __init__(self, documents, numberOfClusters): self.documents, self.means, self.numberOfClusters, self.vectors = documents, [], numberOfClusters, None
    
    def _convertDocumentsToVector(self):
        self.vectors = []
        dimensions = TwoWayMap()
        for docId, document in self.documents:
            for w in document.split(): 
                if not dimensions.contains(EMTextClustering.PHRASE_TO_DIMENSION, w): dimensions.set(EMTextClustering.PHRASE_TO_DIMENSION, w, len(dimensions))
        for docId, document in self.documents:
            vector = zeros(len(dimensions))
            for w in document.split(): vector[dimensions.get(EMTextClustering.PHRASE_TO_DIMENSION, w)]+=1 
            self.vectors.append(vector)
        
    def cluster(self):
        if self.vectors==None: self._convertDocumentsToVector()
        for i in range(self.numberOfClusters): 
            self.means.append(VectorGenerator.getRandomGaussianUnitVector(len(self.vectors[0]), 4, 1).values())
#            self.means.append(ones(len(self.vectors[0])))
        clusterer = cluster.EMClusterer(self.means, bias=0.1) 
        return clusterer.cluster(self.vectors, True, trace=True) 

if __name__ == '__main__':
#    TrainingAndTestDocuments.generate()
    import numpy
    print numpy.zeros(10)
