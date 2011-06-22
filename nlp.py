'''
Created on Jun 14, 2011

@author: kykamath
'''

import enchant, cjson

twitter_stop_words_file='data/stop_words.json'
twitter_stop_words_over_threshold_percentage = 0.5

enchantDict = enchant.Dict("en_US")
def isEnglish(sentance, threshold=0.3):
    data = sentance.split()
    englishWords, totalWords = 0.0, len(data)
    try:
        englishWords = sum(1.0 for w in data if enchantDict.check(w))
    except Exception: pass
    if englishWords/totalWords > threshold: return True
    return False

class StopWords:
    list = None
    @staticmethod
    def load(extra_terms=['#p2', '#ff', '#fb']):
        if StopWords.list == None: 
            StopWords.list = {}
            stop_word_candidates = cjson.load(open(twitter_stop_words_file))
            for stop_word_candidate in stop_word_candidates:
                if stop_word_candidates[stop_word_candidate]['ot'] >= twitter_stop_words_over_threshold_percentage: StopWords.list[stop_word_candidate]=True
            for term in extra_terms: StopWords.list[term] = True
    @staticmethod
    def contains(word):
        try:
            return StopWords.list[word]
        except KeyError: return False