import pandas as pd 
from import_data_csv import *
from sys import exit
from bloomberg2dict import *


"""

		/****************************************
         *                                      *
         *               RSI class              *
         *              Adela Yang              *
         *                                      *
         ****************************************/
        
        Description:    This is a replication of the classic RSI test from the paper: "The Relative Strength Index Revisited" by Adrian Taran-Morosan.
        				RSI is being calculated with an input of 14 days and an entry threshold of 30.
						
						This class calls bloomberg2dict.py which assumes a pre-existing file called bloomberg_data.csv which
						is filled with data in the following format:
						[0]			[1]			[2]			
						date	closing_price	volume      

						There are 1573 days and the file begins on 2/2/2004 to 4/30/2010.
						The RSI test begins on 3/1/2004 to 4/30/2010; 3/1/2004 begins on index 19.

"""

#The initialization of lists from bloomberg file
date = []
close = []
volume = []

#stores the daily RSI values
rsi = []


"""
main function that runs the RSI algorithm with input of n-days (14) and entry threshold (30)
returns:
	b: buy
	s: sell
	n: neither
"""
def mainRSI():
	counterB = 0 #counts the number of buy signals
	counterS = 0 #counts the number of sell signals
	counterN = 0 #counts the number of neither signals

	passedB = False #true if buy signal
	passedS = False #true if sell signal

	entry_threshold = 30 
	n_days = 14

	# RSI calculated by taking account of previous 14 days so initialize the first 14 days to 0 and "n" first
	rsi.extend([0]*n_days)  
	signal = ["n"]*n_days 	#daily signals b,s,n
	transaction = ["n"]*n_days # daily transactions: b,s,n

	aggData = stock2dict() #gets the data of the bloomberg file into a dictionary
	init(aggData) #initialize the dictionary into lists of date, closing price and volume

	RSI(n_days) #calculates and stores daily RSI values

	#please refer to paper for buy/sell signal and transaction cues (p.5858: the first strategy)
	for i in range(n_days, len(date)):
		#accounts for the closing the opening position
		if transaction[i-1] == "b":
			if rsi[i] > 50 or rsi[i] < entry_threshold:
				transaction.append("s")
				signal.append("n")
				passedB = False
				passedS = False
				continue
		elif transaction[i-1] == "s":
			if rsi[i] < 50 or rsi[i] > 100-entry_threshold:
				transaction.append("b")
				signal.append("n")
				passedB = False
				passedS = False
				continue

		#determines the signal
		if rsi[i] < entry_threshold:
			signal.append("b")
			passedB = True
		elif rsi[i] > 100-entry_threshold: 
			signal.append("s")
			passedS = True
		else: 
			signal.append("n")

		#determines the transaction
		if passedB and entry_threshold < rsi[i] and rsi[i] < 50:
			transaction.append("b")
			passedS = False
			passedB = False
			continue
		elif passedB and rsi[i] > 50:
			transaction.append("n")
			passedS = False
			passedB = False
			continue

		if passedS and 50 < rsi[i] and rsi[i] < 100-entry_threshold:
			transaction.append("s")
			passedS = False
			passedB = False
			continue
		elif passedS and rsi < 50:
			transaction.append("n")
			passedB = False
			passedS = False
			continue

		transaction.append("n")

	#starting on day 3/1/2004 which begins on index 19, it counts the number of signals
	for i in range(19,len(date)):
		if signal[i] == "b":
			counterB +=1
		elif signal[i] == "s":
			counterS += 1
		else:
			counterN += 1

	print counterB, counterS, counterN



"""
function takes in n_days = 14
	returns: daily RSI values
This formula is taken from the paper's definition of RSI. This can be found on pages 5856-7.
"""
def RSI(n):
	alpha = 2.0/(n+1.0)
	#the first days cannot be calulcuated
	UC = [0] #up close
	DC = [0] #down close
	#the first 13 days cannot be calculated
	smaU = [0]*(n-1) #simple arithmetic average of up close
	smaD = [0]*(n-1) #simple arithmetic average of down close

	#calculates daily UC,DC 
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

	#calculates daily smaU, smaD 
	for i in range(n-1, len(date)):
		smaU.append(sum(UC[i-13:i+1])/n)				
		smaD.append(sum(DC[i-13:i+1])/n)	

	#calculates daily exponential moving average of up close and down close
	for i in range(n, len(date)):
		emaU = alpha*UC[i] + (1-alpha)*smaU[i-1] 
 		emaD = alpha*DC[i] + (1-alpha)*smaD[i-1] 
 		rs = emaU/emaD #relative strength
		rsi.append(100.0-(100.0/(1+rs)))



"""
take in dictionary
given an input of a dictionary, it extract the columns into the following categories
"""
def init(aggData):
	date.extend(aggData["default_Dates"])
	close.extend(aggData["default_Close"])
	volume.extend(aggData["default_Volume"])


#runs the main function
mainRSI()




















# for i in range(len(aggData.values()[0])):
# date.append(aggData.values()[0][i][0])
