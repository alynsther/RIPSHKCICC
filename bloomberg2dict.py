from csv import *
import csv
import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt
import os

aggregate_csv = []	

stock_dict = {}

heading = ['Dates', 'Open', 'Close', 'RSI_9D', 'RSI_14D', 'RSI_30D']

'''
SUGGESTIONS:
USE THE data_bloomberg.csv FILE AS IMPORT SOURCE
'''

'''
This function converts the .csv file received from bloomberg into a dictionary where key: value is XXXSTOCK_Open : open prices or XXXSTOCK_Close : close prices
It currently only works for certain col/row format of a .csv file just like the excel version I wrote earlier
but it can be modified to accommodate other formats too
This version assumes that the first column is the time of each update of stock price
and the second column refers to the open price, third column refers to the close price of the stock
It still works if the .csv file isn't in this format, just some modifications on several lines of code would fix it.
'''

def stock2dict(file_location_csv, stock_name):
	with open(str(file_location_csv)) as csvfile:														#Importing the csv file into a variable
		read_csv = csv.reader(csvfile, delimiter = ',')
		aggregate_csv.insert(0, heading)
		for row in read_csv:
			del(row[0])
			del(row[6])
			del(row[6])
			aggregate_csv.append(row)
		del aggregate_csv[-5:]
		del aggregate_csv[1]
		try:
			for cell in aggregate_csv:
				if 'Open' not in cell:
					for num in range(1, 6):
						cell[num] = float(cell[num])
		except Exception, e:
			print "C't work: "

	file_location_csv = 'temp.csv'
	with open('temp.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',')
		for row in aggregate_csv:
			writer.writerow(row)

	df = pd.read_csv(file_location_csv)
	try:
		stock_dict[str(stock_name) + '_Dates'] = df['Dates'].tolist()
		stock_dict[str(stock_name) + '_Close'] = df['Close'].tolist()
		stock_dict[str(stock_name) + '_Open'] = df['Open'].tolist()
	except Exception, e:
		print 'Cannot work: '

file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'
stock_name = raw_input('Tell me the name of the stock: ')
stock2dict(file_location_csv, stock_name)
print stock_dict

os.remove('temp.csv')


