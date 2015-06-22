from csv import *
import csv
import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt
import os
import math
import random
import datetime

'''
This program generates a random walk process from a set of historical data and then plot it with the historical data. 
'''

aggregate_csv = []	

stock_dict = {}

simulation_dict = {}

heading = ['Dates', 'Close', 'Volume']

plt.style.use('ggplot')

def stock2dict(file_location_csv, stock_name):
	with open(str(file_location_csv)) as csvfile:														#Importing the csv file into a variable
		read_csv = csv.reader(csvfile, delimiter = ',')

		for row in read_csv:
			aggregate_csv.append(row)
		try:
			for cell in aggregate_csv:
				for num in range(1, 3):
					cell[num] = float(cell[num])
		except Exception, e:
			print str(e)
		aggregate_csv.insert(0, heading)

	file_location_csv = 'temp.csv'
	with open('temp.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',')
		for row in aggregate_csv:
			writer.writerow(row)

	df = pd.read_csv(file_location_csv)
	try:
		stock_dict[str(stock_name) + '_Dates'] = df['Dates'].tolist()
		stock_dict[str(stock_name) + '_Close'] = df['Close'].tolist()
		stock_dict[str(stock_name) + '_Volume'] = df['Volume'].tolist()
	except Exception, e:
		print 'Cannot work: ' + str(e)

def computesigma(historicalPrices): #traditionally, numbers of days should be somewhere between 90 and 180 or the number of days over which we want to do the simulation
    days = len(historicalPrices)
    sum_u = 0
    logreturn = [0] * (days - 1)
    for i in range(days - 1):  #construct a list of log return
        logreturn[i] = math.log(historicalPrices[i + 1] / historicalPrices[i])  #calculate each log return 
        sum_u += logreturn[i]
    average_u = sum_u / (days - 1)   # unbiased estimator of mu of the normal distribution
    sum_difference_square = 0
    for i in range(len(logreturn)):
        sum_difference_square += (logreturn[i] - average_u) ** 2
    v = (sum_difference_square / (len(logreturn) - 1)) ** 0.5     #unbiased estimator of the sd of the normal distribution
    sigma = v / ((1.0 / 252) ** 0.5)  # scale to be the yearly sigma, note that there are usually 252 trading days a year
    return sigma

def computemu(historicalPrices):
    days = len(historicalPrices)
    sum_u = 0
    logreturn = [0] * (days - 1)
    for i in range(days - 1):
        logreturn[i] = math.log(historicalPrices[i + 1] / historicalPrices[i])
        sum_u += logreturn[i]
    average_u = sum_u / (days - 1)#unbiased estimator of mu of the normal distribution
    sigma = computesigma(historicalPrices)
    mu = average_u * 252 + 0.5 * (sigma ** 2)  # result comes from ito's calculus
    return mu
    
def generateWt(t):
    return random.gauss(0, t ** 0.5)  #generate a random variable follows N(0,t)

'''the t is the time period we want to consider and n is how many intermediate
   prices we want to get, so the time step will be t/n
   eg, if we want to get a daily stock price, we can set t=1,n=252 as there are usually 252 trading days a year
   and choose mu to be the yearly drift and sigma to be the yearly violatility
'''
def generateSt(t, n, S0, historicalPrices):
    global stockprices
    stockprices = []    #construct a list of simulated stock prices
    stockprices.append(S0)
    mu = computemu(historicalPrices)#calculate mu from the pre-defined function
    sigma = computesigma(historicalPrices)  #calculate sigma from the pre-defined function
    t = float(t)
    for i in range(1, n + 1):
        stockprices.append(stockprices[i - 1] * (math.exp((mu - sigma ** 2 / 2) * (t / n) + sigma * generateWt(t / n))))
    return stockprices

'''
Main part
'''

file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'
#stock_name = raw_input('Tell me the name of the stock: ')
stock_name = 'Default'
stock2dict(file_location_csv, stock_name)

historicalPrices = stock_dict[str(stock_name) + '_Close']

os.remove('temp.csv')

generateSt(6, len(stock_dict[str(stock_name) + '_Close']) - 1, 1193.19, historicalPrices)
stock_dict[str(stock_name) + '_Simulation'] = stockprices

Date = str(stock_name) + '_Dates'
Close = str(stock_name) + '_Close'
Volume = str(stock_name) + '_Volume'
Sim = str(stock_name) + '_Simulation'


df = pd.DataFrame.from_dict(stock_dict, orient = 'columns')
df[Date] = pd.to_datetime(df[Date])
df2 = df.set_index(str(stock_name) + '_Dates', drop = True)

print df2

df2[Close].plot()
df2[Sim].plot()
plt.show()

