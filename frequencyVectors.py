#encoding=utf8

import numpy

def countWords(strlist):
    worep=""
    for j in range(len(strlist)):
        for i in range(len(strlist[j])):
            if strlist[j][i] not in worep:
                worep+=strlist[j][i]
    print worep
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

string=u"我起来我们困"
string2=u"他他"
string3=u"ad"
strlist=[string,string2,string3]

def calculateCov(frequencyVectors): #,priceVector):
    a=[]
    for i in range(len(frequencyVectors)):
        a.append(frequencyVectors[i])
    #a.append(priceVector)
    x=numpy.array(a).T
    y=numpy.cov(x).tolist()
    length=len(y)
    return y[length-1]
print calculateCov(countWords(strlist))
