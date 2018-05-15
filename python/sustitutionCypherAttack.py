from math import log10
from pycipher import SimpleSubstitution as SimpleSub
import sys
import random
import re

#global variables
Ctext = ''
bestIndv = ''

Ntotal = 0
Lgram = 0
dictionaryNgrams={}
floorValue = 0


maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -9999999999999999999999999999999999

#language ngram stats
def ngrams(file_uut, sep=' '):
    global Ntotal
    global Lgram
    global dictionaryNgrams
    global floorValue
    with open(file_uut) as f:
        for line in f:
            key,value = line.split(sep)
            Ntotal += int(value)
            dictionaryNgrams[key] = value
    keys = dictionaryNgrams.keys()
    Lgram = len(key)
    floorValue = log10(0.01/Ntotal)
    for k in keys:
        relativeValue = log10(float(dictionaryNgrams[k])/Ntotal)
        dictionaryNgrams[k] = relativeValue
    print(dictionaryNgrams['TION'])

#consideramos text_ut no solo contiene caracteres alfabeticos
def fitnessFunction(text_ut):
    #contabilizar los Ngrams del texto y multiplicarlo por su relative value
    value = 0
    for i in range(0,len(text_ut)-(Lgram+1)):
        ngram_ut = text_ut[i:i+Lgram]
        if ngram_ut in dictionaryNgrams:
            value_to_add = dictionaryNgrams[ngram_ut]
        else:
            value_to_add = floorValue
        value += value_to_add
    return value



def getStateScore(key):
    plainText = SimpleSub(key).decipher(Ctext)
    return fitnessFunction(plainText)

def getRandomNeighbour(key):
    copyKey = key[:]
    a = random.randint(0,25)
    b = random.randint(0,25)
    charA = copyKey[a]
    charB = copyKey[b]
    copyKey[a] = charB
    copyKey[b] = charA
    return copyKey


#Stochastic Hill Climbing
#Current <- RandomSolution(ProblemSize)
#for(iter in Iter)
#   Candidate <- RandomNeighbour(Current)
#   if(Cost(Candidate) > Cost(Current))
#       Current <- Candidate
#return Current

def StochasticHillClimbing(x):
    random.shuffle(maxkey)
    currentKey = maxkey[:]
    currentScore = getStateScore(currentKey)
    i = 0
    while i<x:#for i in range(0,x):
        candidateKey = getRandomNeighbour(currentKey)
        candidateScore = getStateScore(candidateKey)
        if(candidateScore > currentScore):
            currentKey = candidateKey
            currentScore = candidateScore
            i=0#si hay mejora continuar hasta que no exista mejoria
        i+=1
    return currentKey,currentScore

#Analisis de frecuencia
def substitutionAttack(text_ut, ngrams_file, iter, x):
    global Ctext
    global bestIndv
    global maxscore
    Ctext = re.sub('[^A-Z]','',text_ut.upper())
    ngrams(ngrams_file)
    for i in range(0,iter):
        currentKey,currentScore = StochasticHillClimbing(x)
        if currentScore > maxscore:
            maxkey = currentKey[:]
            maxscore = currentScore
            plainText = SimpleSub(maxkey).decipher(Ctext)
            print(maxscore)
            print(plainText)



if __name__ == "__main__":
    text= 'lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wibpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jxymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpryjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjklmird jk xjubt trmui jx ibndtwb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbiiwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower mvjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkdwkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbrjx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhriiijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmhmnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlbbpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkdwkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bprriirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb'

    #text = 'pmpafxaikkitprdsikcplifhwceigixkirradfeirdgkipgigudkcekiigpwrpucikceiginasikwduearrxiiqepcceindgmieinpwdfprduppcedoikiqiasafmfddfipfgmdafmfdteiki'
    substitutionAttack(text,sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
