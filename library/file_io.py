'''
Created on Jun 13, 2011

@author: kykamath
'''
import os, cjson

class FileIO:
    @staticmethod
    def createDirectory(path):
        dir = path[:path.rfind('/')]
        if not os.path.exists(dir): os.umask(0), os.makedirs('%s'%dir, 0770)
    @staticmethod
    def writeToFileAsJson(data, file):
        FileIO.createDirectory(file)
        f = open('%s'%file, 'a')
        f.write(cjson.encode(data)+'\n')
        f.close() 