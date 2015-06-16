from pd import *
from import_data_csv import *
from sys import exit
#from __future__ import division

"""
file assumes a pre-existing .csv file filled with data in the following format from import_data_csv or l.csv example
calculates the rsi from input of n days and entry threshold

[0]		[1]		[2]			[3]		[4]		[5]
date	open	last price	RSI_9D	RSI_14D	RSI_30D
"""

#The initialization of lists
date = []
open_price = []
last_price = []
RSI_9D = []
RSI_14D = []
RSI_30D = []


"""
main function that runs the RSI algorithm with input of n-days and entry thresholds
returns:
	b: buy
	s: sell
	n: neither
"""
def mainMA():
	aggData = mainImportDataCsv()
	# entry threshold and n is determined by the user
	shortma = int(raw_input('Enter days to calculate the short average: ')) 
	longma = int(raw_input('Enter the days for the long average: '))
	differencereq = int(raw_input('Enter the difference required between short and long average to buy or sell:'))
	init(aggData)
	ma = MA(shortma, longma)
	if rsi < entry_threshold:
		print("buy")
		return "b"
	elif rsi > 100-entry_threshold: 
		print("sell")
		return "s"
	else:
		print("neither")
		return "n"



#calculates RSI give n-days
def MA(s, l):
	pastprices = []
	SMA = []
	LMA = []
	if s > l:
		print(len(date))
		print(s)
		print(l)
		print("Error: the number of days in your short moving average is longer than your long moving average.")
		exit(0)
	if s > len(date) or l > len(date):
		print(len(date))
		print(s, l)
		print("Error: not enough data")
		exit(0)
	for t in range(len(date)-l, len(date)):
		LMA.append(last_price[t]) 
	for t in range(len(date)-s, len(date)):
		SMA.append(last_price[t])
		#make sure its a float
	shortMA = sum(SMA)/s
	longMA = sum(LMA)/l
	print(shortMA, 'short moving average')
	print(longMA, 'long moving average')
	return shortMA - longMA
	


# given an input of a dictionary, it extract the columns into the following categories
def init(aggData):
	for i in range(len(aggData.values()[0])):
		date.append(aggData.values()[0][i][0])
	for i in range(len(aggData.values()[0])):
		open_price.append(aggData.values()[0][i][1])
	for i in range(len(aggData.values()[0])):
		last_price.append(aggData.values()[0][i][2])
	


mainRSI()