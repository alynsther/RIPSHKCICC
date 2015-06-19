from csv import *
import csv
import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt
import os

aggregate_csv = []	

stock_dict = {}

heading = ['Dates', 'Close', 'Volume']

'''
SUGGESTIONS:
USE THE data_bloomberg.csv FILE AS IMPORT SOURCE
'''

'''
This function converts the .csv file received from bloomberg into a dictionary where key: value is XXXSTOCK_Open : open prices or XXXSTOCK_Close : close prices
Works for the RSI test.
'''

def stock2dict(file_location_csv, stock_name):
	with open(str(file_location_csv)) as csvfile:														#Importing the csv file into a variable
		read_csv = csv.reader(csvfile, delimiter = ',')
		aggregate_csv.insert(0, heading)
		for row in read_csv:
			aggregate_csv.append(row)
		try:
			for cell in aggregate_csv:
				if 'Dates' not in cell:
					for num in range(1, 4):
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
		stock_dict[str(stock_name) + '_Volume'] = df['Volume'].tolist()
	except Exception, e:
		print 'Cannot work: '

file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'
stock_name = raw_input('Tell me the name of the stock: ')
stock2dict(file_location_csv, stock_name)
print stock_dict

os.remove('temp.csv')


