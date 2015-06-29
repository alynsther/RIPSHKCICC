# encoding=utf8

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

letters = {}

letterPositions={"a":[0,0,0,0,1],"b":[0,0,0,1,0],"c":[0,0,0,1,1],"d":[0,0,1,0,0],"e":[0,0,1,0,1],
                 "f":[0,0,1,1,0],"g":[0,0,1,1,1],"h":[0,1,0,0,0],"i":[0,1,0,0,1],"j":[0,1,0,1,0],
                 "k":[0,1,0,1,1],"l":[0,1,1,0,0],"m":[0,1,1,0,1],"n":[0,1,1,1,0],"o":[0,1,1,1,1],
                 "p":[1,0,0,0,0],"q":[1,0,0,0,1],"r":[1,0,0,1,0],"s":[1,0,0,1,1],"t":[1,0,1,0,0],
                 "u":[1,0,1,0,1],"v":[1,0,1,1,0],"w":[1,0,1,1,1],"x":[1,1,0,0,0],"y":[1,1,0,0,1],
                 "z":[1,1,0,1,0]}

def remove_punc(text):
	str_list = word_tokenize(text)
	whole_str = ""

	for i in range(len(str_list)):
	    whole_str += str_list[i]

	string = whole_str.translate(None, ',.!?+-!@#$%^&*'"'"'_()~`{}\|[]:;"<>/1234567890')

	return string

def import_from_txt():
	f = open('sample.txt', 'r')
	text = ''
	for line in f:
		text += line.rstrip()
	text = text.lower()

	return text

def move_points(string):
	positionList = [[0,0,0,0,0]]

	for j in range(len(string)):
		currentPosition = []
		k = string[j]
		for i in range(5):
			currentPosition.append(0.5 * float(int(letterPositions[k][i]) + float(positionList[j][i])))
		#print currentPosition
		positionList.append(currentPosition)

	return positionList

def processing(positionList):
	classPointList = [[0,0,0,0,0]]

	for point in positionList:
		classPoint = []
		for i in range(5):
			classPoint.append(int(float(point[i]) * 3))
		classPointList.append(classPoint)

	return classPointList
		
def classing(classPointList):
    dic={}
    for i in range(3):
            for j in range(3):
                    for k in range(3):
                            for l in range(3):
                                    for m in range(3):
                                            dic[(i,j,k,l,m)]=0
    for point in classPointList:
            dic[(int(point[0])),int(point[1]),int(point[2]),int(point[3]),int(point[4])]+=1
    return dic

def frequencyDic(dic):
    fd={}
    total= sum(dic.values())
    for i in range(3):
            for j in range(3):
                    for k in range(3):
                            for l in range(3):
                                    for m in range(3):
                                            fd[(i,j,k,l,m)]=0
    for key in fd:
            fd[key]=dic[key]/float(total)
    return fd

print classing(processing(move_points(remove_punc(import_from_txt()))))
print frequencyDic(classing(processing(move_points(remove_punc(import_from_txt())))))





