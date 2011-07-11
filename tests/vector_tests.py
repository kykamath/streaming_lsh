'''
Created on Jun 14, 2011
 
@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
import math
from vector import Vector, VectorGenerator

class VectorTests(unittest.TestCase):
    
    def setUp(self):
        self.v1 = Vector({1:1, 2:3})
        self.v2 = Vector({1:4, 2:8})
    
    def test_initialization(self):
        vector = Vector()
        self.assertEqual(vector, {})
        vector = Vector({1:1})
        self.assertEqual(vector, {1:1})
        self.assertEqual(vector.mod(), 1)
    
    def test_dimension(self):
        vector = Vector()
        self.assertEqual(vector.dimension,0)
        vector[10]=10;vector[11]=11
        self.assertEqual(vector.dimension,2)
    
    def test_addition_and_subtraction(self):
        v1, v2 = Vector(), Vector()
        v1[1]=5;v1[2]=10; v2[1]=5;v2[2]=10
        self.assertEqual(v1+v2,{1: 10, 2: 20})
        self.assertEqual(v1-v2,{1: 0, 2: 0})
        v3=Vector()
        v3+=v1; v3+=v2
        self.assertEqual(v3, {1: 10, 2: 20})
    
    def test_dot(self):
        v1 = Vector()
        v1[1]=5;v1[2]=10;
        self.assertEqual(v1.dot({1:5}),25)
        self.assertEqual(v1.dot({1:2,2:1}), 20)
        
    def test_dotWithSmallerVectorWithSubsetDimensions(self):
        v1 = Vector()
        v1[1]=5;v1[2]=10;
        self.assertEqual(v1.dotWithSmallerVectorWithSubsetDimensions({1:5}),25)
        self.assertEqual(v1.dotWithSmallerVectorWithSubsetDimensions({2:1}), 10)
    
    def test_getTopDimensions(self):
        self.assertEqual({2:3, 1:1},self.v1.getTopDimensions(2))
        self.assertEqual({2:8},self.v2.getTopDimensions(1))
        
    def test_mod(self):
        v1 = Vector()
        v1[1]=4;v1[2]=3
        self.assertEqual(v1.mod(), 5)
        
    def test_getNormalizedVector(self):
        v1 = Vector()
        v1[1]=4;v1[2]=3
        self.assertEqual(v1.getNormalizedVector(), {1:0.8, 2:0.6})
        self.assertEqual({1:0.0, 2:0.0}, Vector({1:0.0, 2:0.0}).getNormalizedVector())
        
    def test_divideByScalar(self):
        self.v2.divideByScalar(2)
        self.assertEqual(self.v2, {1:2, 2:4})
    
    def test_cosineSimilarity(self):
        self.assertEqual(math.ceil(self.v1.cosineSimilarity(self.v1)), 1)
        self.assertEqual(Vector({1:1,2:0}).cosineSimilarity(Vector({1:0,2:1})), 0)
    
    def test_getMeanVector(self): 
        self.assertEqual(Vector.getMeanVector([self.v1,self.v2]), Vector({1:5/2., 2:11/2.}))
        self.assertEqual(Vector.getMeanVector([Vector({1:1}), Vector({2:5})]), Vector({1:1/2.,2:5/2.}))
        self.assertEqual(Vector.getMeanVector([Vector(), Vector({2:5})]), Vector({2:5/2.}))
        
class VectorGeneratorDemo:
    @staticmethod
    def getGaussianUnitVector(): VectorGenerator.getRandomGaussianUnitVector(10, 0, 1)
        
if __name__ == '__main__':
    unittest.main()
