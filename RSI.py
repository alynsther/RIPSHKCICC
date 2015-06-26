import pandas as pd 
from import_data_csv import *
from sys import exit
from bloomberg2dict import *
#from __future__ import division

"""
file assumes a pre-existing .csv file filled with data in the following format from import_data_csv or l.csv example
calculates the rsi from input of n days and entry threshold

[0]		[1]		[2]			[3]		[4]		[5]
date	open	last price	RSI_9D	RSI_14D	RSI_30D
"""

#The initialization of lists from bloomberg format, changes depending on file
date = []
close = []
volume = []

rsi = []


"""
main function that runs the RSI algorithm with input of n-days (14) and entry threshold (30)
returns:
	b: buy
	s: sell
	n: neither
"""
def mainRSI():
	counterB = 0
	counterS = 0
	counterN = 0

	entry_threshold = 30 
	n_days = 14
	rsi.extend([0]*n_days)
	signal = ["n"]*n_days

	aggData = stock2dict()
	init(aggData)

	#print len(date)

	RSI(n_days)

	#print len(rsi)

	for i in range(n_days, len(date)):
		if rsi[i] < entry_threshold:
			signal.append("b")
		elif rsi[i] > 100-entry_threshold: 
			signal.append("s")
		else:
			signal.append("n")

	for i in range(19,len(date)):
		if signal[i] == "b":
			counterB +=1
		elif signal[i] == "s":
			counterS += 1
		else:
			counterN += 1

	print counterB, counterS, counterN



def RSI(n):
	alpha = 2.0/(n+1.0)
	#the first element cannot be calulcuated
	UC = [0]
	DC = [0]
	smaU = [0]*(n-1)
	smaD = [0]*(n-1)

	for t in range(1, len(date)):
		if close[t] > close[t-1] :
			UC.append(close[t]-close[t-1]) 
			DC.append(0.0)
		elif close[t] < close[t-1]:
			DC.append(close[t-1]-close[t])
			UC.append(0.0)
		else: 
			UC.append(0.0)
			DC.append(0.0)

	#print len(UC), len(DC)

	for i in range(n-1, len(date)):
		smaU.append(sum(UC[i-13:i+1])/n)				
		smaD.append(sum(DC[i-13:i+1])/n)	

	#print len(smaU), len(smaD)

	for i in range(n, len(date)):
		emaU = alpha*UC[i] + (1-alpha)*smaU[i-1] 
 		emaD = alpha*DC[i] + (1-alpha)*smaD[i-1] 
 		rs = emaU/emaD
		rsi.append(100.0-(100.0/(1+rs)))

	#print len(rsi)
	

#take in dict, adjust accordingly
# given an input of a dictionary, it extract the columns into the following categories
def init(aggData):
	date.extend(aggData["default_Dates"])
	close.extend(aggData["default_Close"])
	volume.extend(aggData["default_Volume"])

	print date[19]


mainRSI()


# for i in range(len(aggData.values()[0])):
# date.append(aggData.values()[0][i][0])
