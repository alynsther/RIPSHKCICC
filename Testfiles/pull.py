import urllib2
import time
import datetime

import pandas as pd 
from pandas import DataFrame

import csv

import matplotlib.pyplot as plt

aggregate_csv = {}

'''
What this program does is:
1. Pull data from Yahoo finance through pandas with the stock name and timespan that you wanted
2. Save the data into a .csv file
3. Convert the format of the data in the .csv file. Make it a dictionary with the stock name as the key and the stock price data as the content
'''

def pulldata(stock, timespan):
	'''
	try:
	'''
	fileline = stock + '.csv'
	url2visit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=' + timespan + '/csv'
	sourcecode = urllib2.urlopen(url2visit).read()
	splitsource = sourcecode.split('\n') 


	for line in splitsource:
		splitline = line.split(',')
		if len(splitline) == 6:
				savefile = open(fileline, 'a')
				line2write = line + '\n'
				savefile.write(line2write)
	'''
	except Exception, e:
		print 'Cannot run because: ' + str(e)
	'''

def import_from_csv(stock2pull):
	file_location_csv = str(stock2pull) + '.csv'	
	with open(file_location_csv) as csvfile:														
		read_csv = csv.reader(csvfile, delimiter = ',')

		for row in read_csv:
			aggregate_csv[stock2pull].append(row)

		for cell in aggregate_csv[stock2pull]:
			if 'values:Timestamp' not in cell:
				print cell[0]
				cell[0] = datetime.datetime.fromtimestamp(int(cell[0])).strftime('%Y-%m-%d %H:%M:%S')
				for num in range(1, 6):
					cell[num] = float(cell[num])
			else:
				cell[0] = 'Timestamp'		


stock2pull = raw_input('Please input the stock name: ')
timespan = raw_input('Please input the timespan(2y for 2 years, 10d for 10 days): ')
pulldata(stock2pull, timespan)

aggregate_csv[str(stock2pull)] = []
import_from_csv(stock2pull)

print aggregate_csv



