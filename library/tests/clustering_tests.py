'''
Created on Jun 21, 2011

@author: kykamath
'''
import sys
from classes import TwoWayMap
sys.path.append('../')
import unittest
from clustering import EvaluationMetrics, EMTextClustering

class EvaluationMetricsTests(unittest.TestCase):
    def setUp(self):
        self.clusters = [['sports', 'sports', 'sports', 'sports'],
                    ['entertainment', 'entertainment', 'sports', 'entertainment'],
                    ['technology', 'technology', 'politics', 'technology'],
                    ['politics', 'politics', 'politics', 'politics']
                    ]
    def test_getValueForClusters(self): self.assertEqual(0.875, EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.purity))
    def test_getValueForClustersWithEmpltyClusters(self): self.assertEqual(0.0, EvaluationMetrics.getValueForClusters([[]], EvaluationMetrics.purity))
    
class EMTextClusteringTests(unittest.TestCase):
    def test_convertDocumentsToVector(self):
        documents = [
                     (1, 'a b c d f g'),
                     (2, 'a b c d t h'),
                     (3, '1 2 3 4 5'),
                     (4, '1 2 3 ')
                     ]
        print EMTextClustering(documents,2).cluster()
if __name__ == '__main__':
    unittest.main()