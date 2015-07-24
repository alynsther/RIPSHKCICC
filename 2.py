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


string_list = []
words = []
lolists = []
alldate = []
datelist = []
dfdatelist = []

tokenizer = RegexpTokenizer(r'\w+')
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")

number = 3
k = 0

'''
2nd part of the program. 

Before running this part, make sure you have:
1. Combined different text files on a day into a big text file (so that every day has one big text file).
2. The big text file should be renamed so that the program can read through days (or you can modify the names inside the program). 

It reads all those big text files through date.
It outputs 4 files: topic_frequency_default.csv, topic_frequency_09.csv, topic_frequency_1.csv and idf.csv. 
'''

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

    
def import_y_m_d(alldate):

    '''
    Grab in the text files based on the date list generated in generate_date() function.
    Besides take another file in based on the date the user inputed, and do all the subsequent prediction. 
    '''

    global string_list, number

    print ' Constructing file base ... '

    number = len(alldate)
    f = [[]] * (len(alldate))
    for i in range(len(alldate)):
        f[i] = open('wsjdate' + str(alldate[i][0])+ '_' + str(alldate[i][1]) + '_' + str(alldate[i][2]) + '.txt', 'r')
        text = ''       
        for line in f[i]:
            text = text + line.decode("utf-8").rstrip() + ','
        text = text.lower()
        string_list.append(text)
        f[i].close()

    print ' File base constructed '


def choosing_num():

    '''
    Generate a list of lists of proper amount of lists to put in the texts.
    '''

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
    pos_tag = {"NN", "VB", "JJ", "RB", "RBR", "RBS", "JJR", "JJS", "NNP", "NNPS", "NNS", "VBD", "VBG", "VBN", "VBP", "VBZ"}
    k = {u'll', u'e', u'm', u're', u'ag', u'u', u's', u't', u'd', u'p', u'f', u've'}
    pos_list = []
    for j in range(number):
        pos = []
        for i in words[j][0:]:
            word_s = nltk.word_tokenize(i)
            if nltk.pos_tag(word_s)[0][1] in pos_tag:
                #print word_s, nltk.pos_tag(word_s)[0]
                pos.append(wordnet_lemmatizer.lemmatize(wordnet_lemmatizer.lemmatize(word_s[0]), pos = 'v'))
            else:
                continue
        pos = [x for x in pos if x not in k]
        pos_list.append(pos)
        print 'File', str(j), 'filtered. '

    print ' Part of speech filtered '

    return pos_list


def file2wo_rept():
    with open('wo_rept_f.csv', 'rU') as wo_rept_f:
        reader = unicodecsv.reader(wo_rept_f, encoding = 'utf-8')
        wo_rept = [rec for rec in csv.reader(wo_rept_f, delimiter = ',')][0]

    return wo_rept


def count_frequency(wo_rept, pos_list):

    '''
    Construct frequency vector based on the list without repetition.
    Count the frequency of each words that appeared in the pos_list.
    Return the big frequency matrix with columns = word's frequency count and rows = every text file.
    '''

    print ' Constructing frequency vector ... '

    frequency = [[]] * len(pos_list)   
    for i in range(len(pos_list)):
        frequency[i] = [pos_list[i].count(word) for word in wo_rept]
        # for j in range(len(wo_rept)):
            # count = pos_list[i].count(wo_rept[j])
            # frequency[i].append(count)           

    print ' Frequency vector constructed '

    return frequency


def topic_matrix2file(TopicMatrix, method):
    np.savetxt('TopicMatrix_' + str(method) + '.csv', TopicMatrix, delimiter=",")


def file2topic_matrix():
    TopicMatrix_default = genfromtxt('TopicMatrix_default.csv', delimiter=',')
    TopicMatrix_09 = genfromtxt('TopicMatrix_09.csv', delimiter=',')
    TopicMatrix_1 = genfromtxt('TopicMatrix_1.csv', delimiter=',')

    return TopicMatrix_default, TopicMatrix_09, TopicMatrix_1


def tfidf(frequency):
    newFrequency = (np.array(frequency).T).tolist()
    l = len(newFrequency[0])
    #wordInDocument = []
    idf = []
    for i in range(len(newFrequency)):
        documentNumber = len([x for x in newFrequency[i] if x != 0])
        # for j in range (l):
        #     if newFrequency[i][j]  != 0:
        #         documentNumber += 1
        #wordInDocument.append(documentNumber)
    
    #for i in range (len(wordInDocument)):
        idf.append(math.log(float(l) /documentNumber))
        
    for i in range (len(newFrequency)):
        newFrequency[i] = [x * idf[i] for x in newFrequency[i]]
        # for j in range (l):
            # newFrequency[i][j] = newFrequency[i][j] * idf[i]
    normalizedFrequency = np.array(newFrequency).T.tolist()
    #normList = []

    for i in range(len(normalizedFrequency)):
        norm = math.sqrt(sum([x ** 2 for x in normalizedFrequency[i]]))
        # norm = 0
        # for j in range(len(normalizedFrequency[i])):
        #     norm += normalizedFrequency[i][j] ** 2
        # norm = math.sqrt(norm)
        #normList.append(norm)
        if norm == 0:
            continue
        normalizedFrequency[i] = [x / norm for x in normalizedFrequency[i]]
        # for j in range(len(normalizedFrequency[i])):
        #     normalizedFrequency[i][j] = normalizedFrequency[i][j] / norm
    finalF = np.array(normalizedFrequency).T.tolist()

    return finalF,idf


def convertToTopicFrequency(TopicMatrix, tfidf_frequency):

    return np.dot(TopicMatrix,tfidf_frequency)


def topic_frequency2file(topic_frequency, method):
    np.savetxt('topic_frequency_' + str(method) + '.csv', topic_frequency, delimiter=",")


def idf2file(idf):
    with open('idf.csv', 'wb') as idf_f:
        writer = unicodecsv.writer(idf_f, encoding = 'utf-8')
        writer.writerows([idf])


def main():
    wo_rept = file2wo_rept()
    TopicMatrix_default, TopicMatrix_09, TopicMatrix_1 = file2topic_matrix()
    generate_date()
    print datelist
    import_y_m_d(alldate)
    print string_list, len(string_list)
    print number
    choosing_num()
    pos_list = process_content(processing_text(string_list))
    frequency = count_frequency(wo_rept, pos_list)
    tfidf_frequency,idf = tfidf(frequency)
    topic_frequency_default = convertToTopicFrequency(TopicMatrix_default, tfidf_frequency)
    topic_frequency_09 = convertToTopicFrequency(TopicMatrix_09, tfidf_frequency)
    topic_frequency_1 = convertToTopicFrequency(TopicMatrix_1, tfidf_frequency)
    topic_frequency2file(topic_frequency_default, 'default')
    topic_frequency2file(topic_frequency_09, '09')
    topic_frequency2file(topic_frequency_1, '1')
    idf2file(idf)

main()



