import numpy
import scipy.cluster
import scipy.spatial
from matplotlib.pyplot import show
import uniout
import math

alist = [[],[],[],[],[],[],[],[],[],[]]

string_list = []
string = ''


punctuations = [u'£¬',u'¡£',u'£¿',u'£¡',u'£»',u'£º',u' ',u'.',u'(',u'¡¢',u'£¨',u'£©',u')',u'-']

for i in range(10):  #this loop reads texts from different files and put them into a list of strings
    alist[i] = open('text' + str(i) + '.txt', 'r')
    string=""
    for line in alist[i]:   #this loop read lines from one single file and put them in one string
        u_line = unicode(line, 'gbk')
        for j in range(len(punctuations)):
            u_line = u_line.replace(punctuations[j], '')

        string += u_line.rstrip()
        #string=string[1:]    in Windows I need this to read text from notepad, but in Mac, Allen doesn't need this
    string_list.append(string)
#print string_list

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
    norm=0
    for i in range(len(strlist)):
        frequency.append([])
    for i in range(len(strlist)):
        for j in range(len(worep)):
            count=strlist[i].count(worep[j])
            frequency[i].append(count)
            norm+=count**2
        norm=math.sqrt(norm)
        
        for j in range(len(frequency[i])):
            frequency[i][j] = frequency[i][j]/norm
            
        frequencyVector.append(dict(zip(worep, frequency[i])))
    print frequency[0]
    return frequency
    

def drawDendrogram(frequencyList):
    frequencyArray = numpy.array(frequencyList)
    condenseDis = scipy.spatial.distance.pdist(frequencyArray,"euclidean")
    square=scipy.spatial.distance.squareform(condenseDis)
    print square
    linkage=scipy.cluster.hierarchy.linkage(condenseDis)
    dendro=scipy.cluster.hierarchy.dendrogram(linkage)
    show()

drawDendrogram(countOccur(string_list, 2))
