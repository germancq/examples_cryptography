from pycipher import SimpleSubstitution as SimpleSub
import random
import re
from ngram_score_1 import ngram_score
fitness = ngram_score('english_quadgrams.txt') # load our quadgram statistics
ctext= 'lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wibpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jxymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpryjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjklmird jk xjubt trmui jx ibndtwb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbiiwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower mvjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkdwkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbrjx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhriiijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmhmnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlbbpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkdwkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bprriirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb'
#ctext='pmpafxaikkitprdsikcplifhwceigixkirradfeirdgkipgigudkcekiigpwrpucikceiginasikwduearrxiiqepcceindgmieinpwdfprduppcedoikiqiasafmfddfipfgmdafmfdteiki'
ctext = re.sub('[^A-Z]','',ctext.upper())

maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -99e9
parentscore,parentkey = maxscore,maxkey[:]
print ("Substitution Cipher solver, you may have to wait several iterations")
print ("for the correct result. Press ctrl+c to exit program.")
# keep going until we are killed by the user
i = 0
#hill-climbing algorithm
while 1:
    i = i+1
    #random initial state
    random.shuffle(parentkey)
    deciphered = SimpleSub(parentkey).decipher(ctext)
    parentscore = fitness.score(deciphered)
    count = 0
    while count < 1000:
        a = random.randint(0,25)
        b = random.randint(0,25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        deciphered = SimpleSub(child).decipher(ctext)
        score = fitness.score(deciphered)
        #print(score)
        # if the child was better, replace the parent with it
        if score > parentscore:
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count+1
    # keep track of best score seen so far
    if parentscore>maxscore:
        maxscore,maxkey = parentscore,parentkey[:]
        print ('\nbest score so far:',maxscore,'on iteration',i)
        ss = SimpleSub(maxkey)
        print ('    best key: '+''.join(maxkey))
        print ('    plaintext: '+ss.decipher(ctext))
