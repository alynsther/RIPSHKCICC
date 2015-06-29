# encoding=utf8

import nltk
import turtle
from nltk.tokenize import sent_tokenize, word_tokenize
import re

letters = {}

currentPosition = [0,0,0,0,0]

positionList = []

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

	string = whole_str.translate(None, ',.!?+-!@#$%^&*'"'"'()~`{}|[]:;"<>/1234567890')
	return string

def import_from_txt():
	f = open('sample.txt', 'r')
	text = ''
	for line in f:
		text += line.rstrip()
	text = text.lower()

	return text

def move_points(string):
	for j in range(len(string)):
		k = string[j]
		for i in range(5):
			currentPosition[i] = 0.5 * float(int(letterPositions[k][i]) + float(currentPosition[i]))
		positionList.append(currentPosition)

def processing(positionList):
	pass

letter = remove_punc(import_from_txt())
move_points(letter)

print positionList


