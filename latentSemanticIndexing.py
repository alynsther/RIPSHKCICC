
import math
import os
from datetime import *
import datetime
import random

import csv
import unicodecsv

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsRegressor
import scipy.cluster
import scipy.spatial

import pandas as pd
from pandas import DataFrame
import pandas.io.data 


string_list = []
words = []
lolists = []
alldate = []
datelist = []
dfdatelist = []

tokenizer = RegexpTokenizer(r'\w+')
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")

number = 0


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def generate_date():
    global alldate, datelist
    global end_year, end_month, end_day, start_year, start_month, start_day

    print '===== Parsing dates ====='

    start_year, start_month, start_day = int(raw_input("Start year: ")), int(raw_input("Start month: ")), int(raw_input("Start day: "))
    end_year, end_month, end_day = int(raw_input("End year: ")), int(raw_input("End month: ")), int(raw_input("End day: "))

    print '===== Dates parsed ====='
    print '===== Generating datelist ====='

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    one_day = datetime.timedelta(days = 1)
    for single_date in daterange(start_date, end_date):
        alldate.append([single_date.year, single_date.month, single_date.day])
        datelist.append(str(single_date.year) + '-' + single_date.strftime('%m') + '-' + single_date.strftime('%d'))

    print '===== Datelist generated ====='


def import_y_m_d(alldate):
    global string_list, number

    print '===== Constructing file base ====='

    number = len(alldate) + 1
    f = [[]] * (len(alldate))
    for i in range(len(alldate)):
        f[i] = open('bloomberg_' +str(alldate[i][0])+ '_' + str(alldate[i][1]) + '_' + str(alldate[i][2]), 'r')
        text = ''		
        for line in f[i]:
            text = text + line.decode("utf-8").rstrip() + ','
        text = text.lower()
    	string_list.append(text)
        f[i].close()

    print '===== File base constructed ====='
    print '===== Importing take-in file ====='

    text_takein = ''
    f_takein = open('bloomberg_2010_12_30', 'r')
    for lines in f_takein:
        lines_dec = lines.decode("utf-8")
        text_takein = text_takein + lines_dec.rstrip() + ','
    string_list.append(text_takein.lower())

    print '===== Take-in file imported ====='

def choosing_num():
    global number
    global lolists

    #number = int(raw_input("Number of posts: ")) + 1
    lolists = [[]] * (number)


def processing_text(string_list): 

    print '===== Tokenizing word list ====='

    wordsList = lolists
    for i in range(number):
        wordsList[i] = tokenizer.tokenize(string_list[i])

    print '===== Word list tokenized ====='

    return wordsList


def process_content(words):

    print '===== Filtering part of speech ====='

    pos_list = []
    for j in range(number):
        pos = []
        for i in words[j][0:]:
            word_s = nltk.word_tokenize(i)
            if  nltk.pos_tag(word_s)[0][1] == "NN" or \
            	nltk.pos_tag(word_s)[0][1] == "VB" or \
            	nltk.pos_tag(word_s)[0][1] == "JJ" or \
            	nltk.pos_tag(word_s)[0][1] == "RB" or \
            	nltk.pos_tag(word_s)[0][1] == "RBR" or \
            	nltk.pos_tag(word_s)[0][1] == "RBS" or \
            	nltk.pos_tag(word_s)[0][1] == "JJR" or \
            	nltk.pos_tag(word_s)[0][1] == "JJS" or \
            	nltk.pos_tag(word_s)[0][1] == "NNP" or \
            	nltk.pos_tag(word_s)[0][1] == "NNPS" or \
            	nltk.pos_tag(word_s)[0][1] == "NNS" or \
            	nltk.pos_tag(word_s)[0][1] == "VBD" or \
            	nltk.pos_tag(word_s)[0][1] == "VBG" or \
            	nltk.pos_tag(word_s)[0][1] == "VBN"  or \
            	nltk.pos_tag(word_s)[0][1] == "VBP" or \
            	nltk.pos_tag(word_s)[0][1] == "VBZ":
            	#print word_s, nltk.pos_tag(word_s)[0]
            	pos.append(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(word_s[0]), pos = 'v'))
            else:
                continue
        for k in [u'll', u'e', u'm', u're', u'ag', u'u', u's', u't', u'd', u'p', u'f', u've']:
            pos = [x for x in pos if x != k]
        pos_list.append(pos)

    print '===== Part of speech filtered ====='

    print pos_list

    return pos_list


def output_pos_list(pos_list):
    with open('pos_list_f.csv', 'wb') as pos_list_f:
        writer = unicodecsv.writer(pos_list_f, encoding = 'utf-8')
        writer.writerows(pos_list)

def input_pos_list():
    with open('pos_list_f.csv', 'rU') as pos_list_f:
        reader = unicodecsv.reader(pos_list_f, encoding = 'utf-8')
        pos_list = list(list(rec) for rec in csv.reader(pos_list_f, delimiter=','))

    return pos_list


#def output_pos_list(pos_list):
    pos_list_f = open('pos_list_f.txt', 'w')
    for line in pos_list:
        pos_list_f.write(line + '\n')
    pos_list_f.close()


#def input_pos_list():
    pos_list = []
    pos_list_f = open('pos_list_f.txt', 'r')
    for line in pos_list_f:
        pos_list.append(str(line.rstrip('\n')))
    pos_list_f.close()

    return pos_list


def build_wo_rept(pos_list):
    wo_rept = []
    for j in range(len(pos_list)):
        for i in range(len(pos_list[j])):
            if pos_list[j][i] not in wo_rept:
                wo_rept.append(pos_list[j][i])

    return wo_rept


def count_frequency(pos_list):

    print '===== Constructing frequency vector ====='

    wo_rept = build_wo_rept(pos_list)
    frequency = []   
    for i in range(len(pos_list)):
        frequency.append([])
    for i in range(len(pos_list)):
        for j in range(len(wo_rept)):
            count = pos_list[i].count(wo_rept[j])
            frequency[i].append(count)           

    print '===== Frequency vector constructed ====='

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
    TopicFrequency = (V.tolist())[:k]
    topicFrequency = (np.array(TopicFrequency).T).tolist()

    return topicFrequency


def findKNN(frequencyVector, newVector):

    print '===== Constructed index list ====='

    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors = 5, metric = "euclidean")
    neigh.fit(samples)
    indexList = neigh.kneighbors(newVector, return_distance = True)

    print '===== Index list constructed ====='

    return indexList


def drawDendrogram(frequencyList):
    frequencyArray = np.array(frequencyList)
    condenseDis = scipy.spatial.distance.pdist(frequencyArray,"euclidean")
    square = scipy.spatial.distance.squareform(condenseDis).tolist()
    print square[:10]


def main():
    frequency = count_frequency(pos_list)
    tfidf_frequency = tfidf(frequency)
    topicFrequency = singularValueDecomposition(tfidf_frequency, 20)
    drawDendrogram(topicFrequency)
    indexList = findKNN(topicFrequency[: len(topicFrequency) - 1], topicFrequency[len(topicFrequency) - 1])
    indices = indexList[1].tolist()[0][1:]
    #drawDendrogram(topicFrequency)

    return indices


def main2(pos_list):
    frequency = count_frequency(pos_list)
    tfidf_frequency = tfidf(frequency)
    topicFrequency = singularValueDecomposition(tfidf_frequency, 20)
    indexList = findKNN(topicFrequency[: len(topicFrequency) - 1], topicFrequency[len(topicFrequency) - 1])
    distances = indexList[0].tolist()[0][1:]

    return distances


def weighter(price_vector, distances):
 
    print '===== Weighting ====='

    weighted = []
    sum_weight = []
    for i in range(len(distances)):
        weighted.append(float(price_vector[i]) / float(distances[i]))
        sum_weight.append(1 / float(distances[i]))
    result = sum(weighted) / sum(sum_weight)

    print '===== Weighted ====='

    return result


def price_finder(indexList):
    sp500 = pd.io.data.get_data_yahoo('%5EGSPC', 
    start = datetime.datetime(start_year, start_month, start_day), 
    end = datetime.datetime(end_year, end_month, end_day))
    for i in range(len(sp500.index)):
        dfdatelist.append(str(sp500.index[i].to_pydatetime().date()))
    price_vector = []
    for i in indexList:
        print i, datelist[i]
        if datelist[i] in dfdatelist:
            print '1'
            price_vector.append(sp500['Close'][datelist[i]])
        elif datelist[i + 1] in dfdatelist:
            print '2'
            price_vector.append(sp500['Close'][datelist[i + 1]])
        elif datelist[i + 2] in dfdatelist:
            print '3'
            price_vector.append(sp500['Close'][datelist[i + 2]])
        elif datelist[i + 3] in dfdatelist:
            print '4'
            price_vector.append(sp500['Close'][datelist[i + 3]])            

    return price_vector

def price_finder_csv(indices):

    print '===== Generating price vector ====='

    price_change = []
    csvdatelist = []
    price_vector = []
    with open('table.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter = ',')
        for row in read_csv:
            price_change.append(float(row[7]))
            csvdatelist.append(str(row[0]))
    for i in indices:
        print datelist[i]
        if datelist[i] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i])])
        elif datelist[i + 1] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i + 1])])
        elif datelist[i + 2] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i + 2])])
        elif datelist[i + 3] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i + 3])])

    print '===== Price vector generated ====='

    return price_vector

generate_date()
'''
import_y_m_d(alldate)
choosing_num()
output_pos_list(process_content(processing_text(string_list)))
#pos_list = process_content(processing_text(string_list))
'''
pos_list = input_pos_list()
indices = main()
distances = main2(pos_list)
price_vector = price_finder_csv(indices)
result = weighter(price_vector, distances)


print price_vector
print "===== Result is ====="
print "=====", result, "====="
print "===== Goodbye ====="
