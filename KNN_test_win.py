#encoding=utf8

import uniout
import numpy as np
from sklearn.neighbors import NearestNeighbors
import math

alist = [[],[],[],[],[],[],[],[],[],[],[]]

string_list = []
string = ''


punctuations = [u'，',u'。',u'？',u'！',u'；',u'：',u' ',u'.',u'(',u'、',u'（',u'）',u')',u'-']

priceVector=[1,2,3,4,5,6,7,8,9,10]

for i in range(10):  
    alist[i] = open('text' + str(i) + '.txt', 'r')
    string=""
    for line in alist[i]:   
        u_line = unicode(line, 'gbk')
        for j in range(len(punctuations)):
            u_line = u_line.replace(punctuations[j], '')

        string += u_line.rstrip()
            
    string_list.append(string)

alist[len(alist)-1]= open('text0' + '.txt', 'r')
string=""
for line in alist[len(alist)-1]:
    u_line = unicode(line, 'gbk')
    for j in range(len(punctuations)):
        u_line = u_line.replace(punctuations[j], '')
    string += u_line.rstrip()
string_list.append(string)


def countWords(strlist,windowLength):
    worep=[]    
    for j in range(len(strlist)):   
        for i in range(len(strlist[j])-int(windowLength) + 1): 
            if strlist[j][i:i+int(windowLength)] not in worep:  
                worep.append(strlist[j][i:i + int(windowLength)])
    return worep   

def countOccur(strlist,windowLength):
    worep=countWords(strlist,windowLength)
    frequency=[]
    norm=0
    for i in range(len(strlist)):
        frequency.append([])
    for i in range(len(strlist)):
        for j in range(len(worep)):
            count=strlist[i].count(worep[j])
            frequency[i].append(count)
            norm+=count**2
        norm=float(math.sqrt(norm))
        
        for j in range(len(frequency[i])):
            frequency[i][j] = frequency[i][j]/norm

    print frequency[0]
    return frequency
    
def findKNN(frequencyVector,newVector):
    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors=5, metric="euclidean")
    neigh.fit(samples)
    indexList = neigh.kneighbors(newVector,return_distance=False).tolist()
    a=neigh.kneighbors(newVector)
    print a
    return indexList

def main(string_list):
    frequency=countOccur(string_list,2)
    indexList=findKNN(frequency[:(len(frequency)-1)],frequency[len(frequency)-1])
    return indexList[0]
    
indexList=main(string_list)

'''print indexList
for i in indexList:
    print string_list[i]
print string_list[len(string_list)-1]
'''
'''
def newPrice(priceVector, indexList):
    s=0
    for i in range(len(indexList)):
        s+=priceVector[indexList[i]]
    newPrice=float(s)/len(indexList)
    return newPrice
print newPrice(priceVector, indexList)
'''
