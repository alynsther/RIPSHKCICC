#gensim
import logging
from gensim import corpora, models, similarities
from pprint import pprint   # pretty-printer
from collections import defaultdict

#Allen's input_pos_list function
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



#this is to see logging events
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#this can be altered; should use PCA to help determine value
NUM_OF_TOPICS = 10



#allen's function that reads in a csv file that cleans the mass of article from wsj into a list of lists
def input_pos_list():
    with open('pos_list_f.csv', 'rU') as pos_list_f:
        reader = unicodecsv.reader(pos_list_f, encoding = 'utf-8')
        pos_list = list(list(rec) for rec in csv.reader(pos_list_f, delimiter=','))

    return pos_list



#courpus of documents
#texts: list of lists containing the cleaned words of each document in its own list
texts = input_pos_list()
print len(texts)

#each workd gets a unique id
dictionary = corpora.Dictionary(texts)
dictionary.save('deerwester.dict') # store the dictionary, for future reference
pprint(dictionary)  #displays how many unique tokens there are
pprint(dictionary.token2id)  # displays the tokens and their unique ids

#doc2bow: counts the number of occurences of each distinct word
	#converts word to its integer id and returns the result as a sparse vector
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('deerwester.mm', corpus) # store to disk, for later use
pprint(corpus)  

dictionary = corpora.Dictionary.load('deerwester.dict')
corpus = corpora.MmCorpus('deerwester.mm')
print(corpus)  #displays the number of documents, unique ids, and the entries



lda = models.LdaModel(corpus, id2word=dictionary, num_topics=NUM_OF_TOPICS)
corpus_lda = lda[corpus]

lda.print_topics(NUM_OF_TOPICS)











# #creating a transformation
# #tfidf is a read-only object to convert any vector from an old representation to a new one
# tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

# # step 2 -- use the model to transform vectors
# corpus_tfidf = tfidf[corpus]
# #for doc in corpus_tfidf:
#     #print(doc)

# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=NUM_OF_TOPICS) # initialize an LSI transformation
# corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

# #transformed tf-idf corpus via lsi into a n-dimensions
# #displays the topics from 0 to n-1
# lsi.print_topics(NUM_OF_TOPICS) 

# #for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#     #print(doc)

# lsi.save('model.lsi') # same for tfidf, lda, ...
# lsi = models.LsiModel.load('model.lsi')

# print NUM_OF_TOPICS




























#For later use....

#CORPUS STREAMING ONE DOCUMENT AT A TIME
"""
class MyCorpus(object):
    def __iter__(self):
        for line in open('mycorpus.txt'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())

corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
pprint(corpus_memory_friendly)

for vector in corpus_memory_friendly: # load one vector into memory at a time
    pprint(vector)
"""
###########################################