'''
Created on Jun 14, 2011

@author: kykamath
'''

import enchant, cjson, re

twitter_stop_words_file='data/stop_words.json'
twitter_stop_words_over_threshold_percentage = 0.5

pattern = re.compile('[\W_]+')
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
        
def getWordsFromRawEnglishMessage(message, check_stop_words=True):
    returnWords = []
    if isEnglish(message.lower()):
        def matchTag(tag): 
                if tag in ['N'] or tag[:2] in ['NN', 'NP', 'NR']: return True
        message = filter(lambda x: not x.startswith('@') and not x.startswith('http:'), message.lower().split())
        for word in message:
            if word[0]=='#': returnWords.append(str('#'+pattern.sub('', word)))
            else: returnWords.append(str(pattern.sub('', word)))
        returnWords = filter(lambda w: len(w)>2, returnWords)
    if check_stop_words: return filter(lambda w: not StopWords.contains(w) and len(w)>2, returnWords)
    else: return filter(lambda w: len(w)>2, returnWords)