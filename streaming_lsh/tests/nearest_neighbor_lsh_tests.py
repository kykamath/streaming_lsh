'''
Created on Sep 16, 2011

@author: kykamath
'''
import sys, unittest
sys.path.append('../')
from nearest_neighbor_lsh import NearestNeighborUsingLSH
from library.file_io import FileIO
from library.vector import Vector
from classes import Document

nns_settings = {'dimensions': 53,
                'signature_length': 13,
                'number_of_permutations': 5,
                'nearest_neighbor_threshold': 0.5}

def createDocumentFromLine(docId, line):
    vector, words = Vector(), line.split()
    for word in words[1:]:
        if word not in vector: vector[word]=1
        else: vector[word]+=1
    return Document(words[0], vector)

class NearestNeighborUsingLSHTests(unittest.TestCase):
    def setUp(self):
        self.nnsLSH = NearestNeighborUsingLSH(**nns_settings)
        self.documents = []
        i = 0
        for line in FileIO.iterateLinesFromFile('../data/streaming.dat'):
            self.documents.append(createDocumentFromLine(None, line)); i+=1
            if i==10: break
            
    def test_nns(self):
        for d in self.documents: 
            self.nnsLSH.update(d)
            self.assertEqual(d.docId, self.nnsLSH.getNearestDocument(d))
        
    
if __name__ == '__main__':
    unittest.main()