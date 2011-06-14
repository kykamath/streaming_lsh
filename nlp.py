'''
Created on Jun 14, 2011

@author: kykamath
'''

import enchant

enchantDict = enchant.Dict("en_US")
def isEnglish(sentance, threshold=0.3):
    data = sentance.split()
    englishWords, totalWords = 0.0, len(data)
    try:
        englishWords = sum(1.0 for w in data if enchantDict.check(w))
    except Exception: pass
    if englishWords/totalWords > threshold: return True
    return False