#gensim
import logging
from gensim import corpora, models, similarities
from pprint import pprint   # pretty-printer
from collections import defaultdict

#for Allen's input_pos_list function
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
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#this can be altered
NUM_OF_TOPICS = 10



#allen's function that reads in a csv file that cleans the mass of article from wsj into a list of lists
def input_pos_list():
    with open('pos_list_f.csv', 'rU') as pos_list_f:
        reader = unicodecsv.reader(pos_list_f, encoding = 'utf-8')
        pos_list = list(list(rec) for rec in csv.reader(pos_list_f, delimiter=','))

    return pos_list


# # corpus of documents
# documents = ["Human machine interface for lab abc computer applications",
#              "A survey of user opinion of computer system response time",
#              "The EPS user interface management system",
#              "System and human system engineering testing of EPS",
#              "Relation of user perceived response time to error measurement",
#              "The generation of random binary unordered trees",
#              "The intersection graph of paths in trees",
#              "Graph minors IV Widths of trees and well quasi ordering",
#              "Graph minors A survey"]

# # remove common words (stoplist), words that only appear once, and tokenize
# #splits on whitespace and lowercase each word
# stoplist = set('for a of the and to in'.split())
# texts = [[word for word in document.lower().split() if word not in stoplist]
#         for document in documents]

# # remove words that appear only once
# frequency = defaultdict(int)
# for text in texts:
#     for token in text:
#         frequency[token] += 1

# texts = [[token for token in text if frequency[token] > 1]
#         for text in texts]


texts = input_pos_list()
print len(texts)

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#this is to see logging events

#corpus of documents
# documents = ["Human machine interface for lab abc computer applications",
#              "A survey of user opinion of computer system response time",
#              "The EPS user interface management system",
#              "System and human system engineering testing of EPS",
#              "Relation of user perceived response time to error measurement",
#              "The generation of random binary unordered trees",
#              "The intersection graph of paths in trees",
#              "Graph minors IV Widths of trees and well quasi ordering",
#              "Graph minors A survey"]

# # remove common words (stoplist), words that only appear once, and tokenize
# #splits on whitespace and lowercase each word
# stoplist = set('for a of the and to in'.split())
# texts = [[word for word in document.lower().split() if word not in stoplist]
#         for document in documents]

# # remove words that appear only once
# frequency = defaultdict(int)
# for text in texts:
#     for token in text:
#         frequency[token] += 1

# texts = [[token for token in text if frequency[token] > 1]
#         for text in texts]

# pprint(texts)


#each workd gets a unique id
dictionary = corpora.Dictionary(texts)
dictionary.save('deerwester.dict') # store the dictionary, for future reference
#pprint(dictionary)
#pprint(dictionary.token2id)

# new_doc = "Human computer interaction"
# new_vec = dictionary.doc2bow(new_doc.lower().split())
# pprint(new_vec) # the word "interaction" does not appear in the dictionary and is ignored
# #doc2bow: counts the number of occurences of each distinct word
	#converts word to its integer id and returns the result as a sparse vector


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('deerwester.mm', corpus) # store to disk, for later use
#pprint(corpus)

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


dictionary = corpora.Dictionary.load('deerwester.dict')
corpus = corpora.MmCorpus('deerwester.mm')
#print(corpus)

#creating a transformation
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

#tfidf is a read-only object to convert any vector from an old representation to a new one
# doc_bow = [(0, 1), (1, 1)]
# print(tfidf[doc_bow]) # step 2 -- use the model to transform vectors

corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
    #print(doc)

################################################# change number of topics here
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=NUM_OF_TOPICS) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

################################################# cab change value here
#transformed tf-idf corpus via lsi into a 2-Ds
lsi.print_topics(NUM_OF_TOPICS)

#for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
    #print(doc)

lsi.save('model.lsi') # same for tfidf, lda, ...
lsi = models.LsiModel.load('model.lsi')

print NUM_OF_TOPICS