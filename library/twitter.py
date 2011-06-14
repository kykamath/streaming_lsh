'''
Created on Jun 14, 2011

@author: kykamath
'''

import cjson, gzip

class TweetFiles:
    @staticmethod
    def iterateTweetsFromGzip(file):
        for line in gzip.open(file, 'rb'): 
            try:
                data = cjson.decode(line)
                if 'text' in data: yield data
            except: pass