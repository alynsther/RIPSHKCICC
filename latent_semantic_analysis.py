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
    f = lolists
    
    for i in range(number):
        f[i] = open('apple' + str(i) + '.txt', 'r')
        text = ''		
        for line in f[i]:
            text += line.decode("gbk").rstrip()
        text = text.lower()
        string_list.append(text)


def processing_text(string_list): 
    wordsList = lolists
    for i in range(len(string_list)):
        wordsList[i] = tokenizer.tokenize(string_list[i])

    return wordsList

def process_content(words):
    pos_list = []
    for j in range(len(string_list)):
        pos = []
        for i in words[j][0:]:
            word_s = nltk.word_tokenize(i)
            pos.append(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(word_s[0]), pos = 'v'))
            """if nltk.pos_tag(word_s)[0][1] == "NN" or\
               nltk.pos_tag(word_s)[0][1] == "NNP" or\
               nltk.pos_tag(word_s)[0][1] == "NNPS" or\
               nltk.pos_tag(word_s)[0][1] == "NNS" or\
               nltk.pos_tag(word_s)[0][1] == "VB" or\
               nltk.pos_tag(word_s)[0][1] == "VBD" or\
               nltk.pos_tag(word_s)[0][1] == "VBG" or\
               nltk.pos_tag(word_s)[0][1] == "VBN" or\
               nltk.pos_tag(word_s)[0][1] == "VBP" or\
               nltk.pos_tag(word_s)[0][1] == "VBZ" or\
               nltk.pos_tag(word_s)[0][1] == "JJ" or\
               nltk.pos_tag(word_s)[0][1] == "RB" or\
               nltk.pos_tag(word_s)[0][1] == "RBR" or\
               nltk.pos_tag(word_s)[0][1] == "RBS" or\
               nltk.pos_tag(word_s)[0][1] == "JJS" or\
               nltk.pos_tag(word_s)[0][1] == "JJR":
            	#print word_s, nltk.pos_tag(word_s)[0]
            	pos.append(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(word_s[0]), pos = 'v'))
            else:
                continue
            """
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
       
    for i in range(len(pos_list)):
        frequency.append([])
    for i in range(len(pos_list)):
        for j in range(len(wo_rept)):
            count = pos_list[i].count(wo_rept[j])
            frequency[i].append(count)
    return frequency

def tfidf(frequency):
    newFrequency = (np.array(frequency).T).tolist()
    l = len(newFrequency[0])
    wordInDocument = []
    for i in range(len(newFrequency)):
        documentNumber = 0
        for j in range (l):
            if newFrequency[i][j]  != 0:
                documentNumber += 1
        wordInDocument.append(documentNumber)
    idf = []
    for i in range (len(wordInDocument)):
        IDF = math.log(float(l) / wordInDocument[i])
        idf.append(IDF)
        
    for i in range (len(newFrequency)):
        for j in range (l):
            newFrequency[i][j] = newFrequency[i][j]*idf[i]
    return newFrequency
    
def singularValueDecomposition(frequency,k):
    a = np.array(frequency)
    U,s,V = np.linalg.svd(a,full_matrices = False)
    TopicFrequency=(V.tolist())[:k]
    topicFrequency=(np.array(TopicFrequency).T).tolist()
    return topicFrequency
    
def findKNN(frequencyVector, newVector):
    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors = 4, metric = "euclidean")
    neigh.fit(samples)
    a = neigh.kneighbors(newVector)
    print a
    indexList = neigh.kneighbors(newVector, return_distance = False).tolist()

    return indexList

def drawDendrogram(frequencyList):
    frequencyArray = np.array(frequencyList)
    condenseDis = scipy.spatial.distance.pdist(frequencyArray,"euclidean")
    square=scipy.spatial.distance.squareform(condenseDis)
    print square
    
def main(i):
    frequency = count_frequency(pos_list)
    tfidf_frequency= tfidf(frequency)
    topicFrequency = singularValueDecomposition(tfidf_frequency,10)
    indexList = findKNN(topicFrequency,topicFrequency[i])
    print topicFrequency
    drawDendrogram(topicFrequency)
    return indexList[0]
    
choosing_num()
import_from_txt()

pos_list = process_content(processing_text(string_list))
#print pos_list
#for i in range(number):
indexList = main(7)
print indexList
