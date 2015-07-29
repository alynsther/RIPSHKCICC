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
import scipy.sparse
from sklearn.preprocessing import normalize



alldate = []
alldate_takein = []
datelist = []
datelist_takein = []

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
    #topic_frequency_09 = genfromtxt('topic_frequency_09.csv', delimiter=',')
    #topic_frequency_1 = genfromtxt('topic_frequency_1.csv', delimiter=',')

    return topic_frequency_default#, topic_frequency_09, topic_frequency_1


def file2idf():
	idf = []
	with open('idf.csv', 'rU') as idf_f:
	    reader = unicodecsv.reader(idf_f, encoding = 'utf-8')
	    idf_ = [rec for rec in csv.reader(idf_f, delimiter = ',')][0]
	for i in range(len(idf_)):
		idf.append(float(idf_[i]))

	return idf



def file2topic_matrix():
    TopicMatrix_default = genfromtxt('TopicMatrix_default.csv', delimiter=',')
    #TopicMatrix_09 = genfromtxt('TopicMatrix_09.csv', delimiter=',')
    #TopicMatrix_1 = genfromtxt('TopicMatrix_1.csv', delimiter=',')

    return TopicMatrix_default#, TopicMatrix_09, TopicMatrix_1


def daterange(start_date, end_date):

    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def generate_date_p():

    global alldate, datelist
    global end_year, end_month, end_day, start_year, start_month, start_day

    start_year, start_month, start_day = 2010, 1, 1
    end_year, end_month, end_day = 2011, 1, 5

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    one_day = datetime.timedelta(days = 1)
    for single_date in daterange(start_date, end_date):
        alldate.append([single_date.year, single_date.month, single_date.day])
        datelist.append(str(single_date.year) + '-' + single_date.strftime('%m') + '-' + single_date.strftime('%d'))


def generate_date_takein():

    global alldate_takein, datelist_takein
    global end_year_takein, end_month_takein, end_day_takein, start_year_takein, start_month_takein, start_day_takein

    start_year_takein, start_month_takein, start_day_takein = int(raw_input(" >>> Start year: ")), int(raw_input(" >>> Start month: ")), int(raw_input(" >>> Start day: "))
    end_year_takein, end_month_takein, end_day_takein = int(raw_input(" >>> End year: ")), int(raw_input(" >>> End month: ")), int(raw_input(" >>> End day: "))

    start_date_takein = datetime.date(start_year_takein, start_month_takein, start_day_takein)
    end_date_takein = datetime.date(end_year_takein, end_month_takein, end_day_takein)
    one_day = datetime.timedelta(days = 1)
    for single_date in daterange(start_date_takein, end_date_takein):
        alldate_takein.append([single_date.year, single_date.month, single_date.day])
        datelist_takein.append(str(single_date.year) + '-' + single_date.strftime('%m') + '-' + single_date.strftime('%d'))


def import_takein(i):

	string = ''

	text_takein = ''
	year_takein = alldate_takein[i][0]
	month_takein = alldate_takein[i][1]
	day_takein = alldate[i][2]
	f_takein = open('wsjdate' + str(year_takein) + '_' + str(month_takein) + '_' + str(day_takein) + '.txt', 'r')
	for lines in f_takein:
	    lines_dec = lines.decode("utf-8")
	    text_takein = text_takein + lines_dec.rstrip() + ','
	string += text_takein.lower()
    
	return string


def processing_text(string): 

    wordsList = tokenizer.tokenize(string)

    return wordsList


def process_content(words):

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

    return pos_list


def file2wo_rept():
    with open('wo_rept_f.csv', 'rU') as wo_rept_f:
        reader = unicodecsv.reader(wo_rept_f, encoding = 'utf-8')
        wo_rept = [rec for rec in csv.reader(wo_rept_f, delimiter = ',')][0]
    pairs = zip(wo_rept, range(len(wo_rept)))
    word2idx = dict(pairs)
    idx2word = dict([(y,x) for x,y in pairs]) 
    del pairs, wo_rept
    return word2idx, idx2word


def count_frequency(word2idx, idx2word, pos_list, documentFrequency):

    #print ' Constructing frequency vector ... '
    counts, rows, cols = [], [], []
    temp = set(word2idx.keys())
    unique, count = np.unique([word2idx[word] for word in pos_list if word in temp], return_counts=True)
    counts.extend(count)
    rows.extend(unique)
    cols.extend([0] * len(unique))
    frequency = scipy.sparse.csr_matrix((counts, (rows, cols)), shape=(len(word2idx), 1))

    del word2idx, idx2word

    print ' ... '

    idf = scipy.sparse.dia_matrix((len(documentFrequency), len(documentFrequency)))
    idf.setdiag(documentFrequency)

    del documentFrequency

    # multiply each row of frequency by a scalar
    idf *= frequency
    frequency = idf

    del idf

    # normalize frequency's rows with l2 norm
    frequency = normalize(frequency, axis=0)

    return frequency


def topicFrequency(TopicMatrix, frequency):
    
    newtopic_frequency = TopicMatrix * frequency
    return newtopic_frequency


def topic_frequency2file(newtopic_frequency):
    np.savetxt('newtopic_frequency_.csv', newtopic_frequency, delimiter=",")


def findKNN(frequencyVector, newVector):

    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors=3, metric="euclidean")
    neigh.fit(samples)
    indexList = neigh.kneighbors(newVector, return_distance=True)

    return indexList


def main_output(i, documentFrequency, TopicMatrix, topic_frequency, word2idx, idx2word):    


    pos_list = process_content(processing_text(import_takein(i)))
    frequency = count_frequency(word2idx, idx2word, pos_list, documentFrequency)
    newtopic_frequency = topicFrequency(TopicMatrix, frequency)
    indexList = findKNN(topic_frequency.T.tolist(), np.array(newtopic_frequency).T.tolist())
    indices = indexList[1].tolist()[0][0:]
    distances = indexList[0].tolist()[0][0:]

    return indices, distances


def price_finder_csv(indices):

    price_change = []
    csvdatelist = []
    price_vector = []
    with open('table.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
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

        print ' ' + str(indices.index(i) + 1) + '. ' +datelist[i], price_vector[indices.index(i)]

    return price_vector


def weighter(price_vector, distances):

    weighted = []
    sum_weight = []
    for i in range(len(distances)):
        if distances[i] != 0:
            weighted.append(float(price_vector[i]) / float(distances[i]))
            sum_weight.append(1 / float(distances[i]))
        else:
            weighted.append(0)
            sum_weight.append(0)
    result = sum(weighted) / sum(sum_weight)

    return result


def output_result(main_result):
    with open('result_idx_dis2.csv', 'wb') as main_result_f:
        writer = unicodecsv.writer(main_result_f, encoding='utf-8')
        writer.writerows(main_result)

def main():  

    main_result = []
    final_result = []
    generate_date_takein()
    generate_date_p()

    word2idx, idx2word = file2wo_rept()
    documentFrequency = file2idf()

    TopicMatrix_default = file2topic_matrix()
    topic_frequency_default = file2topic_frequency()

    '''
    option = raw_input(' >>> Please selected method applied to choose k (a - default, b - 0.9, c - 1): ')
    if option == 'a':
        for i in range(len(alldate_takein)):
            indices, distances = main_output(i, documentFrequency, TopicMatrix_default, topic_frequency_default, word2idx, idx2word)
            main_result.append([indices, distances])
    elif option == 'b':
        for i in range(len(alldate_takein)):
            indices, distances = main_output(i, documentFrequency, TopicMatrix_09, topic_frequency_09, word2idx, idx2word)
            main_result.append([indices, distances])
    elif option == 'c':
        for i in range(len(alldate_takein)):
            indices, distances = main_output(i, documentFrequency, TopicMatrix_1, topic_frequency_1, word2idx, idx2word)
            main_result.append([indices, distances])
    else:
        print ' Ok.'
    '''
    for i in range(len(alldate_takein)):
        indices, distances = main_output(i, documentFrequency, TopicMatrix_default, topic_frequency_default, word2idx, idx2word)
        main_result.append([indices, distances])
        print ' For', datelist_takein[i], 'Nearest Neighbors are: '
        # If wanted to use other methods, add a if statement right here    
        price_vector = price_finder_csv(main_result[i][0])
        final_result.append(weighter(price_vector, main_result[i][1]))

    output_result(main_result)

    print " The prediction of the program says: "
    print " >>>", final_result
    print " Goodbye! "

if __name__ == '__main__':
    main()









