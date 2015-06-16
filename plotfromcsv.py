from csv import *
import csv
import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt
import os

aggregate_csv = []	

heading = ['Dates', 'Open', 'Last_price', 'RSI_9D', 'RSI_14D', 'RSI_30D']

'''
SUGGESTIONS:
USE THE l.csv FILE AS IMPORT SOURCE
'''

'''
This function imports data from a certain sheet in a csv file
It currently only works for certain col/row format of a .csv file just like the excel version I wrote earlier
but it can be modified to accommodate other formats too
This version assumes that the first column is the time of each update of stock price
and the second column refers to the open price, third column refers to the close price of the stock
It still works if the .csv file isn't in this format, just some modifications on several lines of code would fix it.
'''

def import_from_csv():
	file_location_csv = raw_input('Tell me the directory of the .csv file you want to import: ')	#This is asking the for the location of the file
	with open(str(file_location_csv)) as csvfile:														#Importing the csv file into a variable
		read_csv = csv.reader(csvfile, delimiter = ',')

		aggregate_csv.insert(0, heading)

		for row in read_csv:
																					#Reading each row of .csv and append it
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

def export_to_csv(stock2push):
	file_location_csv = str(stock2push) + '.csv'
	with open(file_location_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',')
		for row in aggregate_csv:
			writer.writerow(row)

def pandas_read_csv(stock2read):
	file_location_csv = str(stock2read) + '.csv'
	df = pd.read_csv(file_location_csv, index_col = 'Dates', parse_dates = True)
	print df.head()
	df[['Open', 'Last_price', 'RSI_9D', 'RSI_14D', 'RSI_30D']].plot()
	plt.show()

import_from_csv()
print aggregate_csv 

stock2push = raw_input('Name a file to export the data: ')
export_to_csv(stock2push)

stock2read = raw_input('Stock2read: ')
pandas_read_csv(stock2read)

os.remove(str(stock2push) + '.csv')


