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

from numpy import genfromtxt
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsRegressor
import scipy.cluster
import scipy.spatial


alldate = []
datelist = []
dfdatelist = []

tokenizer = RegexpTokenizer(r'\w+')
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")

k = 0

'''
Final part of the program. This is the final selection part.

Before running this program: 
1. Make sure all the products in 1st and 2nd part are in the same directory. 
2. Make sure there's a csv file containing all the price information (like table.csv). 
3. Make sure that there is a text file to take in. The file should be similar to the big text file in terms of both content and naming(should be all the news on a day). 
4. Change the start/end dates in the generate_date_p() function to a proper date range (refering to the generate_date() function in part 2) 

Good luck
'''

def file2topic_frequency():
    topic_frequency_default = genfromtxt('topic_frequency_default.csv', delimiter=',')
    topic_frequency_09 = genfromtxt('topic_frequency_09.csv', delimiter=',')
    topic_frequency_1 = genfromtxt('topic_frequency_1.csv', delimiter=',')

    return topic_frequency_default, topic_frequency_09, topic_frequency_1


def file2idf():
	idf = []
	with open('idf.csv', 'rU') as idf_f:
	    reader = unicodecsv.reader(idf_f, encoding = 'utf-8')
	    idf_ = [rec for rec in csv.reader(idf_f, delimiter = ',')][0]
	for i in range(len(idf_)):
		idf.append(float(idf_[i]))

	return idf


def file2wo_rept():
    with open('wo_rept_f.csv', 'rU') as wo_rept_f:
        reader = unicodecsv.reader(wo_rept_f, encoding = 'utf-8')
        wo_rept = [rec for rec in csv.reader(wo_rept_f, delimiter = ',')][0]

    return wo_rept


def file2topic_matrix():
    TopicMatrix_default = genfromtxt('TopicMatrix_default.csv', delimiter=',')
    TopicMatrix_09 = genfromtxt('TopicMatrix_09.csv', delimiter=',')
    TopicMatrix_1 = genfromtxt('TopicMatrix_1.csv', delimiter=',')

    return TopicMatrix_default, TopicMatrix_09, TopicMatrix_1


def daterange(start_date, end_date):

    '''
    A function used to construct date range. To be used in generate_date() function.
    '''

    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def generate_date_p():

    '''
    Partial version. Dates are set to default. 2010-1-1 ~ 2011-1-1
    '''

    global alldate, datelist
    global end_year, end_month, end_day, start_year, start_month, start_day

    print ' Parsing dates ... '

    start_year, start_month, start_day = 2010, 1, 1
    end_year, end_month, end_day = 2012, 1, 1

    print ' Dates parsed '
    print ' Generating datelist ... '

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    one_day = datetime.timedelta(days = 1)
    for single_date in daterange(start_date, end_date):
        alldate.append([single_date.year, single_date.month, single_date.day])
        datelist.append(str(single_date.year) + '-' + single_date.strftime('%m') + '-' + single_date.strftime('%d'))

    print ' Datelist generated '


def import_takein():
	string = ''
	print ' Importing take-in file ... '

	text_takein = ''
	year_takin = raw_input(' Please input the year: ')
	month_takin = raw_input(' Please input the month: ')
	day_takin = raw_input(' Please input the day: ')
	f_takein = open('wsjdate' + str(year_takin) + '_' + str(month_takin) + '_' + str(day_takin) + '.txt', 'r')
	for lines in f_takein:
	    lines_dec = lines.decode("utf-8")
	    text_takein = text_takein + lines_dec.rstrip() + ','
	string += text_takein.lower()

	print ' Take-in file imported '
	return string

def processing_text(string): 

    '''
    Tokenize each string from text files.
    Return a list of lists which contains a tokenized sentence namely every words in that sentence.
    '''

    print ' Tokenizing word list ... '
    wordsList = tokenizer.tokenize(string)

    print ' Word list tokenized '

    return wordsList


def process_content(words):

    '''
    Filter the tokenized words in each string by their pos.
    Currently only take into account the verbs and nouns.
    Also lemmatizes words, get rid of plural form and tenses and so on.
    Also removes the 's, 't, 'll... things.
    Return a list of lists which contains every lemmatized words.
    '''

    print ' Filtering part of speech ... '
    pos_tag = {"NN", "VB", "JJ", "RB", "RBR", "RBS", "JJR", "JJS", "NNP", "NNPS", "NNS", "VBD", "VBG", "VBN", "VBP", "VBZ"}
    k = {u'll', u'e', u'm', u're', u'ag', u'u', u's', u't', u'd', u'p', u'f', u've'}
    pos_list = []
    for i in words:
        word_s = nltk.word_tokenize(i)
        if nltk.pos_tag(word_s)[0][1] in pos_tag:
            #print word_s, nltk.pos_tag(word_s)[0]
            pos_list.append(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(word_s[0]), pos = 'v'))
        else:
            continue
    pos_list = [x for x in pos_list if x not in k]

    print ' Part of speech filtered '

    return pos_list


def count_frequency(wo_rept, pos_list):

    '''
    Construct frequency vector based on the list without repetition.
    Count the frequency of each words that appeared in the pos_list.
    Return the big frequency matrix with columns = word's frequency count and rows = every text file.
    '''

    print ' Constructing frequency vector ... '

      
    frequency = [pos_list.count(word) for word in wo_rept]          

    print ' Frequency vector constructed '

    return frequency


def tfidf(frequency,idf):
    for i in range (len(frequency)):
        frequency[i] = frequency[i] * idf[i]
    norm = 0
    for i in range(len(frequency)):
        norm += frequency[i]**2
    norm = math.sqrt(norm)
    for i in range(len(frequency)):
        frequency[i] = frequency[i] / norm

    return frequency


def topicFrequency(TopicMatrix, frequency):
    termFrequency = np.array(frequency).T
    newtopic_frequency = np.dot(TopicMatrix, termFrequency)

    return newtopic_frequency


def findKNN(frequencyVector, newVector):

    '''
    Find the K-nearest neighbors.
    Return a list of two lists.
    The 1st list contains the distances between the selected and the K-nearest, the 2nd list contains the indices of the K-nearest
    '''

    print ' Constructed index list ... '

    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors = 2, metric = "euclidean")
    neigh.fit(samples)
    indexList = neigh.kneighbors(newVector, return_distance = True)

    print ' Index list constructed '

    return indexList


def main_output():    

    '''
    Calling functions.
    Return the indices and distances of the K-nearest.
    '''
    string = import_takein()
    wordsList = processing_text(string)
    pos_list = process_content(wordsList)
    wo_rept = file2wo_rept()
    idf = file2idf()
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency = tfidf(frequency,idf)
    TopicMatrix_default, var2, var3 = file2topic_matrix()
    topic_frequency_default, var2, var3 = file2topic_frequency()
    newtopic_frequency = topicFrequency(TopicMatrix_default, frequency)
    indexList = findKNN(topic_frequency_default.T.tolist(), np.array(newtopic_frequency).T.tolist())
    indices = indexList[1].tolist()[0][0:]
    distances = indexList[0].tolist()[0][0:]

    return indices, distances


def main_output_09():    

    '''
    Calling functions.
    Return the indices and distances of the K-nearest.
    '''
    string = import_takein()
    wordsList = processing_text(string)
    pos_list = process_content(wordsList)
    wo_rept = file2wo_rept()
    idf = file2idf()
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency = tfidf(frequency,idf)
    var1, TopicMatrix_09, var3 = file2topic_matrix()
    var1, topic_frequency_09, var3 = file2topic_frequency()
    newtopic_frequency = topicFrequency(TopicMatrix_09, frequency)
    indexList = findKNN(topic_frequency_09.T.tolist(), np.array(newtopic_frequency).T.tolist())
    indices = indexList[1].tolist()[0][0:]
    distances = indexList[0].tolist()[0][0:]

    return indices, distances


def main_output_1():    

    '''
    Calling functions.
    Return the indices and distances of the K-nearest.
    '''
    string = import_takein()
    wordsList = processing_text(string)
    pos_list = process_content(wordsList)
    wo_rept = file2wo_rept()
    idf = file2idf()
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency = tfidf(frequency,idf)
    var1, var2, TopicMatrix_1 = file2topic_matrix()
    var1, var2, topic_frequency_1 = file2topic_frequency()
    newtopic_frequency = topicFrequency(TopicMatrix_1, frequency)
    indexList = findKNN(topic_frequency_1.T.tolist(), np.array(newtopic_frequency).T.tolist())
    indices = indexList[1].tolist()[0][0:]
    distances = indexList[0].tolist()[0][0:]

    return indices, distances


def price_finder_csv(indices):

    '''
    Find the stock price locally from a csv file exported from yahoo finnance.
    Return the stock prices of the K-nearest neighbors as a list.
    '''

    print ' Generating price vector ... '
    print ' Days taken out with prices are shown below: '

    price_change = []
    csvdatelist = []
    price_vector = []
    with open('table.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter = ',')
        for row in read_csv:
            price_change.append(float(row[7]))
            csvdatelist.append(str(row[0]))
    for i in indices:
        if datelist[i] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i])])
        elif datelist[i + 1] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i + 1])])
        elif datelist[i + 2] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i + 2])])
        elif datelist[i + 3] in csvdatelist:
            price_vector.append(price_change[csvdatelist.index(datelist[i + 3])])
        print ' >>>' + datelist[i], price_vector[indices.index(i)]

    print ' Price vector generated '

    return price_vector


def weighter(price_vector, distances):

    '''
    Weight the price of each K-nearest neighbors wrt their distances (weight = inverse number of distance). 
    Calculate the prediction based on the stock prices and the distances.
    Return the prediction.
    '''
 
    print ' Weighting '

    weighted = []
    sum_weight = []
    for i in range(len(distances)):
        weighted.append(float(price_vector[i]) / float(distances[i]))
        sum_weight.append(1 / float(distances[i]))
    result = sum(weighted) / sum(sum_weight)

    print ' Weighted '

    return result


def main():  

    '''
    Run the program partially in order to reduce runtime.
    Start from taking in input_pos_list(), so that no need to lemmatize and tokenize every time.
    '''

    generate_date_p()
    option = raw_input(' >>> Please selected method applied to choose k (a - default, b - 0.9, c - 1): ')
    if option == 'a':
        indices, distances = main_output()
        print indices, distances
    elif option == 'b':
        indices, distances = main_output_09()
    elif option == 'c':
        indices, distances = main_output_1()
    else:
        print 'Ok.'
    price_vector = price_finder_csv(indices)
    result = weighter(price_vector, distances)

    print " The prediction of the program says: "
    print " >>>", result
    print " Goodbye! "

main()









