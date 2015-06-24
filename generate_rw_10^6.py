from csv import *
import csv
import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt
import os
import math
import random
import datetime
import numpy as np

'''
This program generates a random walk process from a set of historical data and then plot it with the historical data. 
'''

aggregate_csv = []	

stock_dict = {}
simulation_dict = {}

stock_name = 'S&P500'

Date = str(stock_name) + '_Dates'
Close = str(stock_name) + '_Close'
Volume = str(stock_name) + '_Volume'
Sim = str(stock_name) + '_Simulation'

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
		aggregate_csv.insert(0, ['Dates', 'Close', 'Volume'])

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

def simulation():
    simulation_dict['Dates'] = []
    simulation_dict['Original'] = []

    for i in range(64):
        simulation_dict['Dates'].append(stock_dict[Date][252 + i])
        simulation_dict['Original'].append(stock_dict[Close][252 + i])

    r_list = []
    generating_list = []

    for trail in range(100000):
        generating = generateSt(0.25 , 63, 1189.89, stock_dict[str(stock_name) + '_Close'])
        r, n = 0, 0
        while n < 64:
            r += abs(float(generating[n]) - float(simulation_dict['Original'][n]))
            n += 1
        r_list.append(r)
        generating_list.append(generating)

    index = r_list.index(min(r_list))
    print min(r_list), index
    simulation_dict['Simulation'] = generating_list[index]

def plot():
    df = pd.DataFrame.from_dict(simulation_dict, orient = 'columns')
    df['Dates'] = pd.to_datetime(df['Dates'])
    df2 = df.set_index('Dates', drop = True)
    df2['Simulation'].plot()
    df2['Original'].plot()
    plt.legend()
    plt.show()


'''
Main part
'''

file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'

#stock_name = raw_input('Tell me the name of the stock: ')

stock2dict(file_location_csv, stock_name)

os.remove('temp.csv')

simulation()

plot()



