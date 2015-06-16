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
def mainRSI():
	aggData = mainImportDataCsv()
	# entry threshold and n is determined by the user
	entry_threshold = int(raw_input('Enter the Entry Threshold: ')) 
	n_days = int(raw_input('Enter the n-day RSI, where n is an integer: '))
	init(aggData)
	rsi = RSI(n_days)
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
def RSI(n):
	UC = []
	DC = []
	if n > len(date):
		print(len(date))
		print(n)
		print("The number of days is greater than the data available.")
		exit(0)
	for t in range(1, n):
		if last_price[t] > last_price[t-1] :
			UC.append(last_price[t]-last_price[t-1]) 
			DC.append(0.0)
		elif last_price[t] < last_price[t-1]:
			DC.append(last_price[t-1]-last_price[t])
			UC.append(0.0)
		else: 
			UC.append(0.0)
			DC.append(0.0)
	AUC = sum(UC)/n					#make sure its a float
	ADC = sum(DC)/n
	print(AUC, 'AUC')
	print(ADC, 'ADC')
	RS = AUC/ADC
	RSI_t = 100.0-(100.0/(1+RS))
	print (RSI_t, 'RSI')
	return RSI_t

	


# given an input of a dictionary, it extract the columns into the following categories
def init(aggData):
	for i in range(len(aggData.values()[0])):
		date.append(aggData.values()[0][i][0])
	for i in range(len(aggData.values()[0])):
		open_price.append(aggData.values()[0][i][1])
	for i in range(len(aggData.values()[0])):
		last_price.append(aggData.values()[0][i][2])
	for i in range(len(aggData.values()[0])):
		RSI_9D.append(aggData.values()[0][i][3])
	for i in range(len(aggData.values()[0])):
		RSI_14D.append(aggData.values()[0][i][4])
	for i in range(len(aggData.values()[0])):
		RSI_30D.append(aggData.values()[0][i][5])



mainRSI()