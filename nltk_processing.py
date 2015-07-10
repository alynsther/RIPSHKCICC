#encoding=utf8

from nltk.tokenize.stanford_segmenter import StanfordSegmenter
import uniout
import numpy
import os

segmenter = StanfordSegmenter(path_to_jar="stanford-segmenter-3.4.1.jar", path_to_sihan_corpora_dict="./data", path_to_model="./data/pku.gz", path_to_dict="./data/dict-chris6.ser.gz")

alist = [[],[],[],[],[],[],[],[],[],[]]
segmented_list = [[],[],[],[],[],[],[],[],[],[]]
price_list = [22921.89, 23984.14, 23982.61, 24898.11, 25843.78, 27142.47, 27831.52, 28838.37, 29465.05, 30405.22]

punctuations = [u',', u'“', u'”', u'?', u'=', u'”', u':', u'％', u'>', u'…', u'+', u'「', u'」', u'～', u'．', u'■', u'【', u'】', u'，',u'。', u'%',u'？',u'！',u'；',u'：',u' ',u'.',u'(',u'、',u'（',u'）',u')',u'-', u'《', u'》', u'[', u']', u'‰'] + ['"']

def splitter():	
	pooled_list = []

	for i in range(10):
		alist[i] = open('newsample' + str(i) + '.txt', 'r') #
		string = ""
		stringstring = ""
		for line in alist[i]:
		    u_line = unicode(line, 'utf8')
		    for j in range(len(punctuations)):
		        u_line = u_line.replace(punctuations[j], '')
		    string += u_line.rstrip()

		stringstring += string

		segmentedStr = segmenter.segment(stringstring)

		f = open('newSegsample' + str(i) + '.txt', 'w') #
		f.write(segmentedStr.encode('UTF-8')) #
		f.close() #

		segmented_list[i] = segmentedStr.split(' ')

	for i in range(10):
		pooled_list += segmented_list[i]

	return pooled_list

def countWords(strlist):
    worep = []
    for j in range(len(strlist)):
        if strlist[j] not in worep:
            worep.append(strlist[j])
    return worep

def countOccur(strlist):
    worep = countWords(strlist)
    occurrences = []
    #frequencyVector = []
    for i in range(len(strlist)):
        occurrences.append([])
        for j in range(len(worep)):
            occurrences[i].append(strlist[i].count(worep[j]))
            total = float(sum(occurrences[i]))
        for j in range(len(occurrences[i])):
            occurrences[i][j] = occurrences[i][j] / total
        #frequencyVector.append(dict(zip(worep, occurrences[i])))
    #print occurrences
    return occurrences

def calculateCorr(occurrences, priceVector):
    a = []
    for i in range(len(occurrences)):
        a.append(occurrences[i])
    x = numpy.array(a).T
    a = x.tolist()
    a.append(priceVector)
    z = numpy.array(a)
    y = numpy.ma.corrcoef(z)
    m = y.tolist()
    length = len(m)
    return m[length - 1]

# this is without selection return every word and its correlation coefficient
'''def frequencyDict(strlist,price):
    worep=countWords(strlist)
    corrcoef=calculateCorr(countOccur(strlist),price)
    dic={}
    for i in range(len(worep)):
        dic[worep[i]]=corrcoef[i]
    return dic'''

# this selects what is believed to be correlated
def corrDict(strlist, price):
    worep = countWords(strlist)
    corrcoef = calculateCorr(countOccur(strlist),price)
    dic = {}
    for i in range(len(worep)):
        if corrcoef[i] != None and abs(corrcoef[i]) > 0.7:
            dic[worep[i]] = corrcoef[i]
    return dic

splitter()
#countWords(pooled_list, winlen)
#print countOccur(string_list)
#print calculateCorr(countOccur(string_list), percentage)
#print corrDict(splitter(), price_list)



'''
	return word_list

def merger(word_list):
	for i in range(5):
		pool_list = []
		pool_list += word_list[i]

	return pool_list

def pooler(pool_list):
	pooled_list = []
	for i in range(len(pool_list)):
		if pool_list[i] not in pooled_list:
			pooled_list.append(pool_list[i])

	return pooled_list

def counter(pooled_list):
	occurrences = []
	frequencyVector = []
	for i in range(len(pool_list)):
	    occurrences.append([])
	for i in range(len(pool_list)):
	    for j in range(len(pooled_list)):
	        occurrences[i].append(pool_list[i].count(pooled_list[j]))
	        total = float(sum(occurrences[i]))
	    for j in range(len(occurrences[i])):
	        occurrences[i][j] = occurrences[i][j] / total
	    frequencyVector.append(dict(zip(pooled_list, occurrences[i])))

	return occurrences

def calculateCorr(frequencyVectors, priceVector):
	a = []
	for i in range(len(frequencyVectors)):
	    a.append(frequencyVectors[i])
	x = numpy.array(a).T
	a = x.tolist()
	a.append(priceVector)
	z = numpy.array(a)
	y = numpy.ma.corrcoef(z)
	m = y.tolist()
	length = len(m)
	return m[length - 1]

def corrDict(pool_list, price):
	corrcoef = calculateCorr(occurrences, price)
	dic = {}
	for i in range(len(pooled_list)):
	    if corrcoef[i] != None and abs(corrcoef[i]) > 0.7:
	        dic[pooled_list[i]] = corrcoef[i]
	return dic

splitter()

word_list = splitter()
pool_list = merger(word_list)
pooled_list = pooler(pool_list)
occurrences = counter(pooled_list)
print corrDict(pool_list, price_list)

'''



