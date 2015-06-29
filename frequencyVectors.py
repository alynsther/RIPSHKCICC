#encoding=utf8

import numpy

def countWords(strlist):
    worep=""
    for j in range(len(strlist)):
        for i in range(len(strlist[j])):
            if strlist[j][i] not in worep:
                worep+=strlist[j][i]
    return worep

def countOccur(strlist):
    worep=countWords(strlist)
    occurrences=[]
    for i in range(len(strlist)):
        occurrences.append([])
    for i in range(len(strlist)):
        for j in range(len(worep)):
            occurrences[i].append(strlist[i].count(worep[j]))
            total=float(sum(occurrences[i]))
        for j in range(len(occurrences[i])):
            occurrences[i][j] = occurrences[i][j]/total
    return occurrences

def calculateCorr(frequencyVectors,priceVector):
    a=[]
    for i in range(len(frequencyVectors)):
        a.append(frequencyVectors[i])
    x=numpy.array(a).T
    a=x.tolist()
    a.append(priceVector)
    z=numpy.array(a)
    y=numpy.ma.corrcoef(z).tolist()
    length=len(y)
    return y[length-1]

# this is without selection return every word and its correlation coefficient
'''def frequencyDict(strlist,price):
    worep=countWords(strlist)
    corrcoef=calculateCorr(countOccur(strlist),price)
    dic={}
    for i in range(len(worep)):
        dic[worep[i]]=corrcoef[i]
    return dic'''

# this selects what is believed to be correlated
def corrDict(strlist,price):
    worep=countWords(strlist)
    corrcoef=calculateCorr(countOccur(strlist),price)
    dic={}
    for i in range(len(worep)):
        if corrcoef[i] != None and abs(corrcoef[i])>0.6:
            dic[worep[i]]=corrcoef[i]
    return dic

strlist=[u"陈陈一轮",u"陈二轮",u"陈三轮轮轮",u"陈四轮",u"陈五轮"]

print countWords(strlist)
print countOccur(strlist)
print calculateCorr(countOccur(strlist),[0.2,-0.1,-0.05,0.05,0.1])
print corrDict(strlist,[0.2,-0.1,-0.05,0.05,0.1])
