
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

'''
Initiallizing everything...
'''


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
k = 0


def daterange(start_date, end_date):

    '''
    A function used to construct date range. To be used in generate_date() function.
    '''

    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def generate_date():

    '''
    User input a start date and an end date, the function creat a list of dates.
    The list of days will be used to pick out news articles from the file base (numerous text files) and price from price sources.
    '''

    global alldate, datelist
    global end_year, end_month, end_day, start_year, start_month, start_day

    print ' Parsing dates ... '

    start_year, start_month, start_day = int(raw_input(" Start year: ")), int(raw_input(" Start month: ")), int(raw_input(" Start day: "))
    end_year, end_month, end_day = int(raw_input(" End year: ")), int(raw_input(" End month: ")), int(raw_input(" End day: "))

    print ' Dates parsed '
    print ' Generating datelist ... '

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    one_day = datetime.timedelta(days = 1)
    for single_date in daterange(start_date, end_date):
        alldate.append([single_date.year, single_date.month, single_date.day])
        datelist.append(str(single_date.year) + '-' + single_date.strftime('%m') + '-' + single_date.strftime('%d'))

    print ' Datelist generated '


def generate_date_p():

    '''
    Partial version. Dates are set to default. 2010-1-1 ~ 2011-1-1
    '''

    global alldate, datelist
    global end_year, end_month, end_day, start_year, start_month, start_day

    print ' Parsing dates ... '

    start_year, start_month, start_day = 2010, 1, 1
    end_year, end_month, end_day = 2011, 1, 1

    print ' Dates parsed '
    print ' Generating datelist ... '

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    one_day = datetime.timedelta(days = 1)
    for single_date in daterange(start_date, end_date):
        alldate.append([single_date.year, single_date.month, single_date.day])
        datelist.append(str(single_date.year) + '-' + single_date.strftime('%m') + '-' + single_date.strftime('%d'))

    print ' Datelist generated '


def import_y_m_d(alldate):

    '''
    Grab in the text files based on the date list generated in generate_date() function.
    Besides take another file in based on the date the user inputed, and do all the subsequent prediction. 
    '''

    global string_list, number

    print ' Constructing file base ... '

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

    print ' File base constructed '
    print ' Importing take-in file ... '

    text_takein = ''
    year_takin = raw_input(' Please input the year: ')
    month_takin = raw_input(' Please input the month: ')
    day_takin = raw_input(' Please input the day: ')
    f_takein = open('bloomberg_' + str(year_takin) + '_' + str(month_takin) + '_' + str(day_takin), 'r')
    for lines in f_takein:
        lines_dec = lines.decode("utf-8")
        text_takein = text_takein + lines_dec.rstrip() + ','
    string_list.append(text_takein.lower())

    print ' Take-in file imported '

def choosing_num():

    '''
    Generate a list of lists of proper amount of lists to put in the texts.
    '''

    global number
    global lolists

    lolists = [[]] * (number)


def processing_text(string_list): 

    '''
    Tokenize each string from text files.
    Return a list of lists which contains a tokenized sentence namely every words in that sentence.
    '''

    print ' Tokenizing word list ... '

    wordsList = lolists
    for i in range(number):
        wordsList[i] = tokenizer.tokenize(string_list[i])

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

    print ' Part of speech filtered '

    return pos_list


def output_pos_list(pos_list):

    '''
    Output the list of lists returned in process_content() namely pos_list.
    Save it into a .csv file.
    Each line correspond to a single list in the list of lists.
    '''

    with open('pos_list_f.csv', 'wb') as pos_list_f:
        writer = unicodecsv.writer(pos_list_f, encoding = 'utf-8')
        writer.writerows(pos_list)

def input_pos_list():

    '''
    Import the .csv file to the program as a list of lists which is exactly the same as pos_list. 
    Return pos_list.
    '''

    with open('pos_list_f.csv', 'rU') as pos_list_f:
        reader = unicodecsv.reader(pos_list_f, encoding = 'utf-8')
        pos_list = list(list(rec) for rec in csv.reader(pos_list_f, delimiter = ','))

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

    '''
    Building a list based on pos_list.
    The list scans through all the words in the list of lists and append all the words that appeared without repetition
    Return the list with all the words without repetition.
    '''

    wo_rept = []
    for j in range(len(pos_list)):
        for i in range(len(pos_list[j])):
            if pos_list[j][i] not in wo_rept:
                wo_rept.append(pos_list[j][i])

    return wo_rept


def count_frequency(wo_rept, pos_list):

    '''
    Construct frequency vector based on the list without repetition.
    Count the frequency of each words that appeared in the pos_list.
    Return the big frequency matrix with columns = word's frequency count and rows = every text file.
    '''

    print ' Constructing frequency vector ... '

    frequency = []   
    for i in range(len(pos_list)):
        frequency.append([])
    for i in range(len(pos_list)):
        for j in range(len(wo_rept)):
            count = pos_list[i].count(wo_rept[j])
            frequency[i].append(count)           

    print ' Frequency vector constructed '

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
            newFrequency[i][j] = newFrequency[i][j] * idf[i]
    normalizedFrequency = np.array(newFrequency).T.tolist()
    normList = []
    for i in range(len(normalizedFrequency)):
        norm = 0
        for j in range(len(normalizedFrequency[i])):
            norm += normalizedFrequency[i][j] ** 2
        norm = math.sqrt(norm)
        normList.append(norm)
    for i in range(len(normalizedFrequency)):
        for j in range(len(normalizedFrequency[i])):
            normalizedFrequency[i][j] = normalizedFrequency[i][j] / normList[i]
    finalF = np.array(normalizedFrequency).T.tolist()

    return finalF
    
def singularValueDecomposition(frequency, k):
    a = np.array(frequency)
    U, s, V = np.linalg.svd(a,full_matrices = False)
    for i in range(len(s)):
        for j in range(len(V[i])):
            V[i][j] = V[i][j] * s[i]
    TopicFrequency = (V.tolist())[:k]
    topicFrequency = (np.array(TopicFrequency).T).tolist()

    return topicFrequency, U


def singularValueDecomposition_09(frequency):
    a = np.array(frequency)
    U, s, V = np.linalg.svd(a, full_matrices = False)
    print s
    for i in range(len(s)):
        for j in range(len(V[i])):
            V[i][j]= V[i][j] * s[i]
    EigenValues = []
    for i in range(len(s)):
        EigenValues.append(s[i] ** 2)
    sumEigenvalues = sum(EigenValues)
    k = 0
    cumulativeSum = 0
    for i in range(len(s)):
        cumulativeSum += EigenValues[i]
        k += 1
        if float(cumulativeSum) / sumEigenvalues >= 0.9:
            break
    print k
    TopicFrequency = (V.tolist())[:k]
    topicFrequency = (np.array(TopicFrequency).T).tolist()

    return topicFrequency, U, k


def singularValueDecomposition_1(frequency):
    a = np.array(frequency)
    U, s, V = np.linalg.svd(a, full_matrices = False)
    print s
    for i in range(len(s)):
        for j in range(len(V[i])):
            V[i][j] = V[i][j] * s[i]
    k = 0
    for i in range(len(s)):
        if s[i] > 1:
            k += 1
    print k
    TopicFrequency = (V.tolist())[:k]
    topicFrequency = (np.array(TopicFrequency).T).tolist()

    return topicFrequency, U, k


def findKNN(frequencyVector, newVector):

    '''
    Find the K-nearest neighbors.
    Return a list of two lists.
    The 1st list contains the distances between the selected and the K-nearest, the 2nd list contains the indices of the K-nearest
    '''

    print ' Constructed index list ... '

    samples = np.array(frequencyVector)
    neigh = NearestNeighbors(n_neighbors = 5, metric = "euclidean")
    neigh.fit(samples)
    indexList = neigh.kneighbors(newVector, return_distance = True)

    print ' Index list constructed '

    return indexList


def drawDendrogram(frequencyList):

    '''
    Draw a dendrogram.
    '''

    frequencyArray = np.array(frequencyList)
    condenseDis = scipy.spatial.distance.pdist(frequencyArray,"euclidean")
    square = scipy.spatial.distance.squareform(condenseDis).tolist()
    print square[:10]


def showTopic(wo_rept, num_topic, U, len_topic):

    '''
    Print the topics. 
    '''

    termWeight = np.array(U).T.tolist()
    topic = []
    for i in range(num_topic):
        topicTuple = dict(zip(wo_rept,termWeight[i])).items()
        topicTuple.sort(key = lambda x: abs(x[1]))
        topicTuple.reverse()
        sortedTopic = topicTuple[:len_topic]
        topic.append(sortedTopic)
        print " Topic",len(topic),"contains: ",topic[len(topic) - 1]


def main_output(pos_list):    

    '''
    Calling functions.
    Return the indices and distances of the K-nearest.
    '''

    wo_rept = build_wo_rept(pos_list)
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency= tfidf(frequency)
    topicFrequency, U = singularValueDecomposition(tfidf_frequency, 2)
    showTopic(wo_rept, 2, U, 10)
    indexList = findKNN(topicFrequency[: len(topicFrequency) - 1], topicFrequency[len(topicFrequency) - 1])
    indices = indexList[1].tolist()[0][1:]
    distances = indexList[0].tolist()[0][1:]

    return indices, distances


def main_output_09(pos_list):    

    '''
    Calling functions.
    Return the indices and distances of the K-nearest.
    '''

    wo_rept = build_wo_rept(pos_list)
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency= tfidf(frequency)
    topicFrequency, U, k = singularValueDecomposition_09(tfidf_frequency)
    showTopic(wo_rept, k, U, 10)
    indexList = findKNN(topicFrequency[: len(topicFrequency) - 1], topicFrequency[len(topicFrequency) - 1])
    indices = indexList[1].tolist()[0][1:]
    distances = indexList[0].tolist()[0][1:]

    return indices, distances


def main_output_1(pos_list):    

    '''
    Calling functions.
    Return the indices and distances of the K-nearest.
    '''

    wo_rept = build_wo_rept(pos_list)
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency= tfidf(frequency)
    topicFrequency, U, k = singularValueDecomposition_1(tfidf_frequency)
    showTopic(wo_rept, k, U, 10)
    indexList = findKNN(topicFrequency[: len(topicFrequency) - 1], topicFrequency[len(topicFrequency) - 1])
    indices = indexList[1].tolist()[0][1:]
    distances = indexList[0].tolist()[0][1:]

    return indices, distances


def price_finder(indexList):

    '''
    Find the stock price online from yahoo finnance.
    Return the stock prices of the K-nearest neighbors as a list.
    '''

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


def main_partial():  

    '''
    Run the program partially in order to reduce runtime.
    Start from taking in input_pos_list(), so that no need to lemmatize and tokenize every time.
    '''

    generate_date_p()
    pos_list = input_pos_list()
    option = raw_input(' >>> Please selected method applied to choose k (a - default, b - 0.9, c - 1): ')
    if option == 'a':
        indices, distances = main_output(pos_list)
    elif option == 'b':
        indices, distances = main_output_09(pos_list)
    elif option == 'c':
        indices, distances = main_output_1(pos_list)
    else:
        print 'Ok.'
    price_vector = price_finder_csv(indices)
    result = weighter(price_vector, distances)

    print " The prediction of the program says: "
    print " >>>", result
    print " Goodbye! "


def main_whole():

    '''
    Run the whole program.
    Get rid of exporting and importing.
    '''

    generate_date()
    import_y_m_d(alldate)
    choosing_num()
    pos_list = process_content(processing_text(string_list))
    option = raw_input(' >>> Please selected method applied to choose k (a - default, b - 0.9, c - 1): ')
    if option == 'a':
        indices, distances = main_output(pos_list)
    elif option == 'b':
        indices, distances = main_output_09(pos_list)
    elif option == 'c':
        indices, distances = main_output_1(pos_list)
    else:
        print 'Ok.'
    price_vector = price_finder_csv(indices)
    result = weighter(price_vector, distances)

    print " The prediction of the program says: "
    print " >>>", result
    print " Goodbye! "


def main():

    '''
    Yeah. 
    '''

    order = raw_input(" >>> Run whole or partial (w/p): ")
    if order == 'w':
        main_whole()
    elif order == 'p':
        main_partial()


main()