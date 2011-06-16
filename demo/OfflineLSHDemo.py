'''
Created on Jun 15, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
from library.vector import Vector
from collections import defaultdict

def iterateLinesFromFile(filePath):
    for line in open('../data/training.dat'):
        if not line.startswith('#'): yield line.strip()

def createVectorFromLine(line):
    vector = Vector()
    for word in line.split()[1:]:
        if word not in vector: vector[word]=0
        vector[word]+=1
    return vector
    

class OfflineLSHDemo:
    @staticmethod
    def demo():
        documents = [createVectorFromLine(l) for l in iterateLinesFromFile('../data/training.dat')]
        print documents
if __name__ == '__main__':
    OfflineLSHDemo.demo()
            