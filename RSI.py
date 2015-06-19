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

#The initialization of lists from bloomberg format
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
	entry_threshold = float(raw_input('Enter the Entry Threshold: ')) 
	while entry_threshold < 0 or entry_threshold > 100:
		print("The entry threshold is out of bounds, it needs to be between 0-100.")
		entry_threshold = int(raw_input('Enter the Entry Threshold: ')) 

	n_days = int(raw_input('Enter the n-day RSI, where n is an integer: '))
	#check if n is within range
	while n_days-1 > len(date) or n_days < 1:
		print("The number of days is greater than the data available or it is invalid.")
		n_days = int(raw_input('Enter the n-day RSI, where n is an integer: '))

	rsi = [0]*n_days
	signal = ["n"]*n_days
	init(aggData)
	
	rsi = rsi + RSI(n_days)
	for i in range(n, len(date))
	if rsi[i] < entry_threshold:
		signal.append("b")
	elif rsi[i] > 100-entry_threshold: 
		signal.append("s")
	else:
		signal.append("n")



#calculates RSI give n-days
def RSI(n):
	#the first element cannot be calulcuated
	UC = [0]
	DC = [0]
	
	for t in range(1, len(date)):
		if last_price[t] > last_price[t-1] :
			UC.append(last_price[t]-last_price[t-1]) 
			DC.append(0.0)
		elif last_price[t] < last_price[t-1]:
			DC.append(last_price[t-1]-last_price[t])
			UC.append(0.0)
		else: 
			UC.append(0.0)
			DC.append(0.0)
	for i in range(n, len(date))
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