'''
Created on Jun 14, 2011

@author: kykamath
'''

import cjson, gzip
from datetime import datetime

class TweetFiles:
    @staticmethod
    def iterateTweetsFromGzip(file):
        for line in gzip.open(file, 'rb'): 
            try:
                data = cjson.decode(line)
                if 'text' in data: yield data
            except: pass
        
@staticmethod
def getDateTimeObjectFromTweetTimestamp(timeStamp): return datetime.strptime(timeStamp, '%a %b %d %H:%M:%S +0000 %Y')