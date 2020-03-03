#coding = utf-8

from __future__ import division
import os
import pickle
import re
import sys
import json



import sys
reload(sys)
# sys.setdefaultencoding('unicode')


N = 1
curDir = os.getcwd()
model_file = "hmmmodel.txt"
input_path = os.path.join(os.getcwd(),"hmm-training-data")
ittrain = "it_isdt_train_tagged.txt"
jatrain = "ja_gsd_train_tagged.txt"
tags = {}
initial = {}
trans = {}
end = {}
emission = {}
initialP = {}
transP = {}
endP = {}
emissionP = {}
initialNum = 0



class modelPara:
    def __init__(self, initialP, transP, endP, emission,tagNum,tags,transN,emissionNum,endNum,initialNum,wordNum):
        self.initialP = initialP
        self.transP = transP
        self.endP = endP
        self.emission = emission
        self.tagNum = tagNum
        self.tags = tags
        self.transN = transN
        self.emissionNum = emissionNum
        self.endNum = endNum
        self.initialNum = initialNum
        self.wordNum = wordNum


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def train(input_path):
    last = ''
    initialNum = 0
    transNum = 0
    endNum = 0
    emissionNum = 0
    tagNum = 0
    transN = 0
    wordNum = 0


    f = open(os.path.join(input_path, ittrain), 'r')
    for line in f.readlines():
        line = line.decode('utf-8')
        line = line.strip()
        # print line
        # line = line.lower()
        # line = "#HEAD#/#HEAD " + line + " #END#/#END#"
        wordlist = re.split(" ",line)

        for index in range(0,len(wordlist)):
            wordNum += 1
            pair = re.split("/",wordlist[index])
            word = ''
            transN +=1
            for i in range(len(pair)):
                if i < len(pair)-1:
                    word += pair[i]
                else:
                    tag = pair[i]
            if is_number(word):
                word = '#NUM'
            word = word.lower()
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1
                tagNum +=1
            #initial
            if index == 0:
                initialNum += 1
                if tag in initial:
                    initial[tag] += 1
                else:
                    initial[tag] = 1
            #trans
            if (index > 0):
                tmp = last + "->" + tag
                if tmp in trans:
                    trans[tmp] +=1
                else:
                    trans[tmp] = 1
            #end
            last = tag
            if (index == (len(wordlist) - 1)):
                endNum += 1
                if (tag in end):
                    end[tag] += 1
                else:
                    end[tag] = 1
            #emission
            emissionNum += 1
            if word in emission:
                if tag in emission[word]:
                    emission[word][tag] += 1
                else:
                    emission[word][tag] =1
            else:
                emission[word] = {tag : 1}




    #get toTag Nums
    tagToNum = {}
    for pairs in trans:
        pair = re.split('->',pairs)
        first = pair[0]
        sec = pair[1]
        if first in tagToNum:
            tagToNum[first] += trans[pairs]
        else:
            tagToNum[first] = trans[pairs]

    #normalization
    for i in tags:
        if i in initial:
            initialP[i] = (float)(initial[i]) / (initialNum + tagNum)
        else:
            initialP[i] = 1.0 / (initialNum+tagNum)
    for i in tags:
        if i in end:
            endi = end[i] + 1.0
        else:
            endi = 1.0

        if i in tagToNum:
            tagtoi = tagToNum[i] + 1.0
        else:
            tagtoi = 1.0
        endP[i] = (float)(endi)/(tagNum + endi + tagtoi)
        #     if i in tagToNum:
        #         endP[i] = (float)(end[i] + 1) / (tagNum + end[i] + tagToNum[i])
        #     else:
        #         endP[i] = (float)(end[i] + 1) / (tagNum + end[i])
        # else:
        #     if i in tagToNum:
        #         endP[i] = (float)(1) / (tagNum + tagToNum[i])
        #     else:
        #         endP[i] = (float)(1) / (tagNum)

    for i in tags:
        for j in tags:
            tmp = i+'->'+j
            if i in tagToNum:
                tagtonum = tagToNum[i] + 1
            else:
                tagtonum = 1

            if j in end:
                endj = end[j] + 1
            else:
                endj = 1
            if tmp in trans:
                transtmp = trans[tmp] + 1
            else:
                transtmp = 1
            transP[tmp] = (float)(transtmp) / (tagNum + endj + tagtonum)


            # if tmp in trans:
            #     if j in end:
            #         transP[tmp] = (float)(trans[tmp] + 1) / (tagNum  + end[j] + tagToNum[i] )
            #     else:
            #         transP[tmp] = (float)(trans[tmp] + 1) / (tagNum + tagToNum[i])
            # else:
            #     if j in end:
            #         transP[tmp] = (float)(1) / (tagNum  + end[j] + tagToNum[i] )
            #     else:
            #         transP[tmp] = (float)(1) / (tagNum + tagToNum[i])


    # for i in trans:
    #     first = re.split('->',i)[1]
    #     if sec in end:
    #         transP[i] = (float)(trans[i] + 1) / (1 + end[first] + tagToNum[first])
    #     else:
    #         transP[i] = (float)(trans[i] + 1) / (1 + tagToNum[first])


    tagEmission = {}
    for word in emission:
        for tag in emission[word]:
            # tag  = (float)(tag) / emissionNum
            if tag in tagEmission:
                tagEmission[tag] += emission[word][tag]
            else:
                tagEmission[tag] = emission[word][tag]

    for word in emission:
        for tag in tags:
            if tag in emission[word]:
                emissionCurTag = emission[word][tag]
            else:
                emissionCurTag = 0.00000001
            emission[word][tag] = (float)(emissionCurTag) / (tagEmission[tag] + wordNum)
    model = modelPara(initialP,transP,endP,emission,tagNum,tags,transN,emissionNum,endNum,initialNum,wordNum)
    # print model.emission
    with open(os.path.join(curDir, model_file), 'wb')as f:
        json.dump(model.__dict__,f)
    return
#



if __name__ == "__main__":

    # input_path = sys.argv[1]
    # voc = set()
    # readStop(os.path.join(os.getcwd(),"stop"))
    train(input_path)

