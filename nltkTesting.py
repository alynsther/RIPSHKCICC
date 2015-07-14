import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.neighbors import NearestNeighbors
import scipy.cluster
import scipy.spatial
import math

string_list = []
tokenizer = RegexpTokenizer(r'\w+')
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")
words = []
lolists = []
number = 10

def choosing_num():
    global number
    global lolists

    number = int(raw_input("Number of posts: "))
    lolists = [[]] * number

def import_from_txt():
    global string_list

    text_takein = ''
    f = lolists
    f_takein = []
    for i in range(number - 1):
        f[i] = open('textEng' + str(i) + '.txt', 'r')
        text = ''		
        for line in f[i]:
            text += line.decode("utf-8").rstrip()
        text = text.lower()
    	string_list.append(text)
    f_takein = open('takein.txt', 'r')
    for lines in f_takein:
        text_takein += lines.decode("utf-8").rstrip()
	text_takein = text_takein.lower()
	string_list.append(text_takein)

def processing_text(string_list): 
    wordsList = lolists
    for i in range(number):
        wordsList[i] = tokenizer.tokenize(string_list[i])

    return wordsList

def process_content(words):
    pos_list = []
    for j in range(number):
        pos = []
        for i in words[j][0:]:
            word_s = nltk.word_tokenize(i)
            if nltk.pos_tag(word_s)[0][1] == "NN" or nltk.pos_tag(word_s)[0][1] == "NNP" or nltk.pos_tag(word_s)[0][1] == "NNPS" or nltk.pos_tag(word_s)[0][1] == "NNS" or nltk.pos_tag(word_s)[0][1] == "VB":
            	#print word_s, nltk.pos_tag(word_s)[0]
            	pos.append(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(word_s[0]), pos = 'v'))
            else:
                continue
        for k in [u'll', u'e', u'm', u're', u'ag', u'u', u's', u't', u'd', u'p', u'f', u've']:
            pos = [x for x in pos if x != k]
        pos_list.append(pos)

    return pos_list

def build_wo_rept(pos_list):
    wo_rept = []
    for j in range(len(pos_list)):
        for i in range(len(pos_list[j])):
            if pos_list[j][i] not in wo_rept:
                wo_rept.append(pos_list[j][i])

    return wo_rept

def count_frequency(pos_list):
    wo_rept = build_wo_rept(pos_list)
    frequency = []
    norm = 0    
    for i in range(len(pos_list)):
        frequency.append([])
    for i in range(len(pos_list)):
        for j in range(len(wo_rept)):
            count = pos_list[i].count(wo_rept[j])
            frequency[i].append(count)
            norm += count ** 2
        norm = math.sqrt(norm)
        for j in range(len(frequency[i])):
            frequency[i][j] = frequency[i][j] / norm

    return frequency

def findKNN(frequencyVector, newVector):
    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors = 5, metric = "euclidean")
    neigh.fit(samples)
    indexList = neigh.kneighbors(newVector, return_distance = False).tolist()

    return indexList

def drawDendrogram(frequencyList):
    frequencyArray = np.array(frequencyList)
    condenseDis = scipy.spatial.distance.pdist(frequencyArray,"euclidean")
    square = scipy.spatial.distance.squareform(condenseDis)
    print square

def main(selected_list):
    frequency = count_frequency(pos_list)
    indexList = findKNN(frequency[:(len(frequency) - 1)],frequency[len(frequency) - 1])

    return indexList[0]
    

choosing_num()
import_from_txt()
pos_list = process_content(processing_text(string_list))
print pos_list
indexList = main(pos_list)

drawDendrogram(count_frequency(pos_list))

print indexList



