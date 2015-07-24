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

import threading
import gc

import sys


string_list = []
words = []
lolists = []
alldate = []
datelist = []
dfdatelist = []

tokenizer = RegexpTokenizer(r'\w+')
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")

number = 14952
k = 0

'''
First part of the program.

It reads a sequence of files from 0 ~ number (represented by the variable 'number'), which are all the files you have (every day, every file)
It outputs 4 .csv files: TopicMatrix_default.csv, TopicMatrix_09.csv, TopicMatrix_1.csv and wo_rept_f.csv. Those files are used in 2nd part.
'''

#consider using an array for linear algebra


def import_wsj():

    '''
    Grab in the text files based on the date list generated in generate_date() function.
    Besides take another file in based on the date the user inputed, and do all the subsequent prediction. 
    '''

    global string_list

    print ' Constructing file base ... '

    f = [[]] * int(number)
    for j in range(number):
        f[j] = open('wsj_' +str(j)+ '.txt', 'r')
        text = ''       
        for line in f[j]:
            text = text + line.decode("utf-8").rstrip() + ','
        text = text.lower()
        string_list.append(text)
        f[j].close()

        #A
        del text

    #A
    del f
    gc.collect()

    print ' File base constructed '
    print ' Importing take-in file ... '
    #print ' Total amount of text (in bytes): %d' sys.getsizeof(string_list)


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

        if j%100 == 0:
            print 'File', str(j), 'filtered. '

        #A

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

    print 'Reading csv file'

    with open('pos_list_f.csv', 'rU') as pos_list_f:
        reader = unicodecsv.reader(pos_list_f, encoding = 'utf-8')
        pos_list = list(list(rec) for rec in csv.reader(pos_list_f, delimiter = ','))


    print 'Finished reading csv file'

    return pos_list



def build_wo_rept(pos_list):

    '''
    Building a list based on pos_list.
    The list scans through all the words in the list of lists and append all the words that appeared without repetition
    Return the list with all the words without repetition.
    '''

    print 'Building wo rept'

    wo_rept = []
    for j in range(len(pos_list)):
        for i in range(len(pos_list[j])):
            if pos_list[j][i] not in wo_rept:
                wo_rept.append(pos_list[j][i])

    return wo_rept

#changes made here according to julien's suggestion
def count_frequency(wo_rept, pos_list):

    '''
    Construct frequency vector based on the list without repetition.
    Count the frequency of each words that appeared in the pos_list.
    Return the big frequency matrix with columns = word's frequency count and rows = every text file.
    '''

    print ' Constructing frequency vector ... '

    frequency = [[]] * len(pos_list)   
    for i in range(len(pos_list)):
        # J: very very slow in theory: list.count is linear in len(list)
        #     and you're calling it len(wo_rept) times

        frequency[i] = [pos_list[i].count(word) for word in wo_rept]

    #faster maybe:
    """
    frequency = [[0] * len(wo_rept)] * len(pos_list)

    for i in range(len(pos_list)):
        for word, j in enumerate(pos_list):
            frequency[i][j] += 1
    """


        # for j in range(len(wo_rept)):
            # count = pos_list[i].count(wo_rept[j])
            # frequency[i].append(count)           

    print ' Frequency vector constructed '

    return frequency


def tfidf(frequency):
    newFrequency = (np.array(frequency).T).tolist()
    l = len(newFrequency[0])
    #wordInDocument = []
    #idf = []
    for i in range(len(newFrequency)):
        print str(i)
        # documentNumber = 0
        documentNumber = len([x for x in newFrequency[i] if x])
        # for j in range (l):
        #     if newFrequency[i][j]  != 0:
        #         documentNumber += 1
        #wordInDocument.append(documentNumber)
    
    #for i in range (len(wordInDocument)):
        #idf.append(math.log(float(l) /documentNumber))
        
    #for i in range (len(newFrequency)):
        newFrequency[i] = [x * (math.log(float(l) /documentNumber)) for x in newFrequency[i]]

        #A
        del documentNumber

        # for j in range (l):
            # newFrequency[i][j] = newFrequency[i][j] * idf[i]
    normalizedFrequency = np.array(newFrequency).T.tolist()
    #normList = []

    #A
    del newFrequency
    gc.collect()



    for i in range(len(normalizedFrequency)):
        print str(i)
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

        #A
        del norm

    finalF = np.array(normalizedFrequency).T.tolist()

    #A
    del normalizedFrequency
    gc.collect()

    return finalF

    
def singularValueDecomposition(frequency, k):

    a = np.array(frequency)
    U, s, V = np.linalg.svd(a,full_matrices = False)
    allTopicMatrix = np.array(U).T
    TopicMatrix = np.array(allTopicMatrix.tolist()[:k])

    #A
    del a
    del U, s, V
    del allTopicMatrix
    gc.collect()

    return TopicMatrix


def singularValueDecomposition_09(frequency):

    a = np.array(frequency)
    U, s, V = np.linalg.svd(a, full_matrices = False)
    for i in range(len(s)):
        V[i]= [x*s[i] for x in V[i]]

    EigenValues = [x**2 for x in s]

    sumEigenvalues = sum(EigenValues)


    cumulativeSum = k = 0
    for i in range(len(s)):
        cumulativeSum += EigenValues[i]
        if float(cumulativeSum) / sumEigenvalues >= 0.9:
            k = i + 1
            break

    allTopicMatrix = np.array(U).T
    TopicMatrix = np.array(allTopicMatrix.tolist()[:k])

    #A
    del a
    del U, s, V
    del EigenValues
    del sumEigenvalues
    del cumulativeSum
    del allTopicMatrix
    gc.collect()

    return TopicMatrix


def singularValueDecomposition_1(frequency):

    a = np.array(frequency)
    U, s, V = np.linalg.svd(a, full_matrices = False)
    for i in range(len(s)):
        V[i]= [x*s[i] for x in V[i]]

    k = len([x for x in s if x > 1])
    # for i in range(len(s)):
    #     if s[i] > 1:
    #         k += 1
    allTopicMatrix = np.array(U).T
    TopicMatrix = np.array(allTopicMatrix.tolist()[:k])

    #A
    del a
    del U, s, V
    del allTopicMatrix
    gc.collect()

    return TopicMatrix

def showTopic(wo_rept, TopicMatrix, len_topic):
    topic = []
    for i in range(TopicMatrix.shape[0]):
        topicTuple = dict(zip(wo_rept, TopicMatrix.tolist()[i])).items()
        topicTuple.sort(key=lambda x:-1*abs(x[1]))
        sortedTopic = topicTuple[:len_topic]
        topic.append(sortedTopic)
        #print "Topic", len(topic), "contains: ", topic[len(topic)-1]

        #A
        del topicTuple
        del sortedTopic

    gc.collect()


def wo_rept2file(wo_rept):
    with open('wo_rept_f.csv', 'wb') as pos_list_f:
        writer = unicodecsv.writer(pos_list_f, encoding = 'utf-8')
        writer.writerows([wo_rept])


def file2wo_rept():
    with open('wo_rept_f.csv', 'rU') as wo_rept_f:
        reader = unicodecsv.reader(wo_rept_f, encoding = 'utf-8')
        wo_rept = [rec for rec in csv.reader(wo_rept_f, delimiter = ',')][0]

    return wo_rept


def topic_matrix2file(TopicMatrix, method):
    np.savetxt('TopicMatrix_' + str(method) + '.csv', TopicMatrix, delimiter=",")


def file2topic_matrix():
    delim = ','

    default_t = threading.Thread(target=process, args=('TopicMatrix_default.csv', delim))
    onine_t = threading.Thread(target=process, args=('TopicMatrix_09.csv', delim))
    one_t = threading.Thread(target=process, args=('TopicMatrix_1.csv', delim))

    default_t.start()
    onine_t.start()
    one_t.start()

    default_t.join()
    onine_t.join()
    one_t.join()

    # TopicMatrix_default = genfromtxt('TopicMatrix_default.csv', delimiter=delim)
    # TopicMatrix_09 = genfromtxt('TopicMatrix_09.csv', delimiter=',')
    # TopicMatrix_1 = genfromtxt('TopicMatrix_1.csv', delimiter=',')
    # return TopicMatrix_default, TopicMatrix_09, TopicMatrix_1

def process(filename, delim):
    genfromtxt(filename, delimiter=delim)



def main():

    # import_wsj()
    # choosing_num()
    # pos_list = process_content(processing_text(string_list))

    # #A
    # gc.collect()

    # output_pos_list(pos_list)

    #A
    # gc.collect()
    pos_list = input_pos_list()
    
    wo_rept = build_wo_rept(pos_list)

    #A
    gc.collect()
    
    wo_rept2file(wo_rept)
    frequency = count_frequency(wo_rept, pos_list)

    #A
    gc.collect()
    
    tfidf_frequency = tfidf(frequency)
    TopicMatrix = singularValueDecomposition(tfidf_frequency, 2)
    showTopic(wo_rept, TopicMatrix, 10)
    topic_matrix2file(TopicMatrix, 'default')
    TopicMatrix_09 = singularValueDecomposition_09(tfidf_frequency)
    showTopic(wo_rept, TopicMatrix_09, 10)
    topic_matrix2file(TopicMatrix_09, '09')
    TopicMatrix_1 = singularValueDecomposition_1(tfidf_frequency)
    showTopic(wo_rept, TopicMatrix_1, 10)
    topic_matrix2file(TopicMatrix_1, '1')

    file2topic_matrix()


main()
