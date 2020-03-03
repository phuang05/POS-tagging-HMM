#coding = UTF-8
# use this file to classify using naive-bayes classifier
# Expected: generate nboutput.txt

from __future__ import division


from hmmlearn2 import modelPara
from numpy import *
import pickle
import sys
import os
import json
import re
import hmmlearn
import sys
reload(sys)
sys.setdefaultencoding('utf8')




model = modelPara({},{},{},{},{},{},int,int,int,int,int)
inputPath = os.path.join( os.getcwd(),"hmm-training-data","it_isdt_dev_raw.txt")
# inputPath = os.path.join(os.getcwd(),"hmm-training-data","ja_gsd_dev_raw.txt")
modelPath = 'hmmmodel.txt'
outputN = 0
wordNum = 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def loadfile(file):
    inputPath = os.path.join(os.getcwd(),file)
    input = open(inputPath,'r')
    return input



def getInitial(tag):
    initialP = model.initialP
    initialNum = model.initialNum

    if tag in initialP:
        return initialP[tag]
    else:
        return 1.0 / (initialNum + model.tagNum)

def getTrans(v, s, u):
    suN = getTran(s, u)
    uvN = getTran(u, v)
    return suN * uvN


def getTran(s,u):
    transP = model.transP
    su = s+'->'+u
    tagNum = model.tagNum
    if su in transP:
        suN = (transP[su]* tagNum + 1.0) / tagNum
    else:
        suN = 1.0/tagNum
    # print s,u,suN
    return suN


def getEndP(s):
    end = model.endP
    endNum = model.endNum
    tagNum = model.tagNum
    if s in end:
        return (end[s] * tagNum+ 1.0) / tagNum
    else:
        return 1.0/tagNum


def getEmission(word, tag):
    if is_number(word):
        word = '#NUM'
    word = word.lower()
    emission = model.emission
    tagNum = model.tagNum
    global wordNum
    # print wordNum
    # print word,tag
    if word in emission:
        # print emission[word][tag]
        return emission[word][tag]

    else:
        return 0.00000001
    # if word in emission:
    #     if tag in emission[word]:
    #         # print (emission[word][tag] * tagNum + 1.0) / model.tagNum
    #         return (emission[word][tag] * tagNum + 1.0) / model.tagNum

    # return 1.0/model.tagNum


def viterbi(model,line,output):
    global outputN
    noOfTag = 0
    score = 0
    line =  line.decode('utf-8')
    line = line.strip()
    words = line.split()
    T = len(words)
    h , w = model.tagNum + 1, T + 1
    viterbi = [[[0 for x in range(h)]for y in range(h)]for z in range(w)]
    backtrack = [['' for x in range(h)]for y in range(w)]
    tags = model.tags
    initialP = model.initialP
    emission = model.emission
    transP = model.transP
    endP = model.endP
    indexT = {}
    index = 0
    for i in tags:
        indexT[i] = index
        index += 1

    tmp = 0
    tmpV = ''
    tmpU = ''
    tmpS = ''




    tmpFirst = inf
    for initial in tags:

        emissionTmp = getEmission(words[0],initial)
        # for tag in tags:
        # viterbi[0][0][indexT[initial]] = 1 * getInitial(initial) * emissionTmp
        viterbi[0][0][indexT[initial]] = -log( getInitial(initial)) - log( emissionTmp)
        if viterbi[0][0][indexT[initial]] < tmpFirst:
            tmpFirst = viterbi[0][0][indexT[initial]]
            tmpV = initial
            # print tmp
    tmpend = inf
    tmpEndTag = ''
    leng = len(words)
    for end in tags:
        emissionTmp = - getEmission(words[leng-1],end)
        viterbi[leng][1][indexT[end]] = -log( getEndP(end)) - log(emissionTmp)
        if viterbi[leng][1][indexT[end]] < tmpend:
            tmpend = viterbi[i][1][indexT[end]]
            tmpEndTag = end



    for i in range(0,len(words) - 1):
        for u in tags:
            emissionTmp = getEmission(words[i],u)
            for v in tags:
                tmp = viterbi[i+1][1][indexT[v]]-log( getTran(u,v)) -log( emissionTmp)
                # print tmp
                if (viterbi[i][1][indexT[u]] == 0) or (tmp < viterbi[i][1][indexT[u]]):
                    viterbi[i][1][indexT[u]] = tmp



    for i in range(len(words)):
            tmpWord = inf
            # print tmp
            # print words[i]
            for v in tags:
                emissionTmp = getEmission(words[i],v)
                for u in tags:

                    tmp = viterbi[i-1][0][indexT[u]]-log( getTran(u,v)) -log( emissionTmp)
                    tmp += viterbi[i-1][1][indexT[u]]
                    # print tmp
                    if (viterbi[i][0][indexT[v]] == 0) or (tmp < viterbi[i][0][indexT[v]]):
                        viterbi[i][0][indexT[v]] = tmp
                        backtrack[i][indexT[v]] = u
                    # if tmp < tmpWord:
                    #     tmpWord = tmp
                    #     tmpV = v







    t = ''
    # t = words[i]+'/'+tmpV + ' '+ t
    t = words[i] + '/' + tmpEndTag + ' '+t
    for i in range(len(words) - 1,0,-1):
        # print words[i]+'/'+tmpV
        t = words[i]+'/'+tmpV + ' '+ t
        tmpV = backtrack[i][indexT[tmpV]]
    t = words[0] + '/' + tmpV + ' '+t
    output.write(t)
    # print t
    output.write("\n")
    outputN = outputN + 1
    print (outputN)
    return


if __name__ == "__main__":
    # global wordNum
    model_file = "hmmmodel.txt"
    output_file = "hmmoutput.txt"
    pkl_file = open(os.path.join(os.getcwd(), "hmmmodel.txt"),'rb')

    model.__dict__ = json.load(pkl_file)
    wordNum = 1.0 / model.wordNum
    output = open(os.path.join(os.getcwd(),output_file),"w")
    # print viterbi(model,"una sala ha dovuto essere sgomberata per una fuga di gas tossico da una scultura moderna in vetro che simboleggia ' i pericoli di la vita ' .")
    input = open(inputPath,'r')
    for line in input:
        # viterbi(model,"I tre avevano da poco lasciato la cima e stavano cominciando la discesa .",output)
        viterbi(model,line,output)