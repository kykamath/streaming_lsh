'''
Created on Jun 21, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from clustering import EvaluationMetrics

class EvaluationMetricsTests(unittest.TestCase):
    def setUp(self):
        self.clusters = [['sports', 'sports', 'sports', 'sports'],
                    ['entertainment', 'entertainment', 'sports', 'entertainment'],
                    ['technology', 'technology', 'politics', 'technology'],
                    ['politics', 'politics', 'politics', 'politics']
                    ]
    def test_getValueForClusters(self):
        self.assertEquals(0.875, EvaluationMetrics.getValueForClusters(self.clusters, EvaluationMetrics.purity))
        
if __name__ == '__main__':
    unittest.main()