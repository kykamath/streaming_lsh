'''
Created on Jun 13, 2011

@author: kykamath
'''
import os, cjson

class FileIO:
    
    @staticmethod
    def createDirectoryForFile(path):
        dir = path[:path.rfind('/')]
        if not os.path.exists(dir): os.umask(0), os.makedirs('%s'%dir, 0777)
    
    @staticmethod
    def writeToFileAsJson(data, file):
        FileIO.createDirectoryForFile(file)
        f = open('%s'%file, 'a')
        f.write(cjson.encode(data)+'\n')
        f.close()
    
    @staticmethod
    def iterateJsonFromFile(file):
        for line in open(file): 
            try:
                yield cjson.decode(line)
            except: pass
    
    @staticmethod
    def getFileByDay(currentTime): return '_'.join([str(currentTime.year), str(currentTime.month), str(currentTime.day)])
    
    @staticmethod
    def iterateLinesFromFile(filePath, commentCharacter='#'):
        for line in open(filePath):
            if not line.startswith(commentCharacter): yield line.strip()