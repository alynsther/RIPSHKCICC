#encoding=utf8

import numpy    #this module is used in calculating correlation coefficient matrix

import uniout   #this module is used to directly print chinese characters instead of the codes

alist = [[],[],[],[],[]]

string_list = []
string = ''


punctuations = [u'，',u'。',u'？',u'！',u'；',u'：',u' ',u'.',u'(',u'、',u'（',u'）',u')',u'-']

for i in range(5):  #this loop reads texts from different files and put them into a list of strings
    alist[i] = open('sample' + str(i) + '.txt', 'r')
    string=""
    for line in alist[i]:   #this loop read lines from one single file and put them in one string
        u_line = unicode(line, 'utf8')
        for j in range(len(punctuations)):
            u_line = u_line.replace(punctuations[j], '')

        string += u_line.rstrip()
        string=string[1:]   #in Windows I need this to read text from notepad, but in Mac, Allen doesn't need this
    string_list.append(string)
print string_list


def countWords(strlist,windowLength):
    worep=[]    #worep means w/o repetition, it contains all different phrases which appear in at least one file
    for j in range(len(strlist)):   #loop through all strings
        for i in range(len(strlist[j])-int(windowLength) + 1):  #loop through all phrases of a single string
            if strlist[j][i:i+int(windowLength)] not in worep:  #here the phrase it 3-character long, but the length can be changed
                worep.append(strlist[j][i:i + int(windowLength)])
    return worep   # it is a string contains all different phrases

def countOccur(strlist,windowLength):
    worep=countWords(strlist,windowLength)
    frequency=[]    #this is a list of lists which contain the frequency of different words in one day
    frequencyVector=[]  #this is a list of  dictionaries, key is the phrase and value is the frequency of different phrases in one day
    countVector=[]  #this is a list of  dictionaries, key is the phrase and value is the number of different phrases in one day
    for i in range(len(strlist)):
        frequency.append([])
    for i in range(len(strlist)):
        for j in range(len(worep)):
            frequency[i].append(strlist[i].count(worep[j]))
            total=float(sum(frequency[i]))
        countVector.append(dict(zip(worep, frequency[i])))
        for j in range(len(frequency[i])):
            frequency[i][j] = frequency[i][j]/total
        frequencyVector.append(dict(zip(worep, frequency[i])))
    print countVector
    print frequencyVector
    return frequency   # we only pass the list i.e. the value of frequency to the next function

def calculateCorr(frequencyVectors,priceVector):
    a=[]
    for i in range(len(frequencyVectors)):
        a.append(frequencyVectors[i])
    x=numpy.array(a).T
    a=x.tolist()
    a.append(priceVector)
    z=numpy.array(a)
    y=numpy.ma.corrcoef(z).tolist()   #from numpy module, this method can calculate the correlation coefficients of an array and returns a list
    length=len(y)
    return y[length-1]   # we only want the item of the list, which contains the corr between phrase frequency and stock prices 

# this is without selection return every word and its correlation coefficient
'''def frequencyDict(strlist,price):
    worep=countWords(strlist)
    corrcoef=calculateCorr(countOccur(strlist),price)
    dic={}
    for i in range(len(worep)):
        dic[worep[i]]=corrcoef[i]
    return dic'''

# this selects what is believed to be correlated and absolute value of corr must be greater than 0.8, this value can be changed
def corrDict(strlist,price,windowLength):
    worep=countWords(strlist,windowLength)
    corrcoef=calculateCorr(countOccur(strlist,windowLength),price)
    dic={}
    for i in range(len(worep)):
        if corrcoef[i] != None and abs(corrcoef[i])>0.8:
            dic[worep[i]]=corrcoef[i]
    return dic

price=[80.44,88.83,87.82,87.08,87.74]   # type in the price list
windowLength=raw_input("Input the window length you want to use: ")   #input the window length

#print countWords(string_list,windowLength)
#print countOccur(string_list,windowLength)
#print calculateCorr(countOccur(string_list,windowLength),price)


print corrDict(string_list,price,windowLength)
