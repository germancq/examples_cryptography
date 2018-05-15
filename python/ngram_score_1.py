'''
Allows scoring of text using n-gram probabilities
17/07/12
'''
from math import log10

class ngram_score(object):
    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        with open(ngramfile) as f:
            for line in f:
                key,count = line.split(sep)
                self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        print(self.N)
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)

        self.floor = log10(0.01/self.N)
        print(self.ngrams['TION'])


    def score(self,text):
        #contabilizar los Ngrams del texto y multiplicarlo por su relative value
        value = 0
        for i in range(0,len(text)-(self.L+1)):
            ngram_ut = text[i:i+self.L]
            #ngrams = self.ngrams.__getitem__
            if ngram_ut in self.ngrams:
                value_to_add = self.ngrams[ngram_ut]
            else:
                value_to_add = self.floor
            value += value_to_add
        return value

    #def score(self,text):
    #    ''' compute the score of text '''
    #    score = 0
    #    ngrams = self.ngrams.__getitem__
    #    for i in range(len(text)-self.L+1):
    #        if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
    #        else: score += self.floor
    #    return score
