'''
Created on Jun 16, 2011

@author: kykamath
'''

from library.file_io import FileIO 

class OnlineLSHDemo:
    @staticmethod
    def demo():
        for line in FileIO.iterateLinesFromFile('../data/streaming.dat'):
            print line

if __name__ == '__main__':
    OnlineLSHDemo().demo()