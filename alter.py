import urllib2
import time
import datetime
import pandas as pd 
from pandas import DataFrame
import csv
import matplotlib.pyplot as plt

aggregate_csv = {}

'''
IMPORTANT:
IN THIS VERSION, YOU HAVE TO DEL THE .CSV FILES GENERATED IN THE SAME FOLDER
FOR INSTANCE,
IF I PULLED 'AAPL' WHEN ASKED 'Please input the stock name: ', AND TYPED XXX WHEN ASKED 'Name a file to import the data: '
YOU HAVE TO DELETE AAPL.csv AND XXX.csv AFTER RUNNING THE PROGRAM.
'''

'''
What this program does is:
1. Pull data from Yahoo finance through pandas with the stock name and timespan that you wanted
2. Make the data a dataframe so that it looks pretty and easy to handle
3. Save it to a .csv file
4. Plot the .csv file
Problems:
1. Currently can only receive data of the last n days/years but not a specfic time interval(the end point of the interval has to be today)
2. Can only handle DataFrame for a certain format

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

def import_from_csv_d(stock2pull):
	file_location_csv = str(stock2pull) + '.csv'	
	with open(file_location_csv) as csvfile:														
		read_csv = csv.reader(csvfile, delimiter = ',')

		for row in read_csv:
			aggregate_csv[stock2pull].append(row)

		for cell in aggregate_csv[stock2pull]:
			if 'values:Timestamp' not in cell:
				cell[0] = datetime.datetime.fromtimestamp(int(cell[0])).strftime('%Y-%m-%d-%H:%M:%S') 
				for num in range(1, 6):
					cell[num] = float(cell[num])
			else:
				cell[0] = 'Dates'		

def import_from_csv_y(stock2pull):
	file_location_csv = str(stock2pull) + '.csv'	
	with open(file_location_csv) as csvfile:														
		read_csv = csv.reader(csvfile, delimiter = ',')

		for row in read_csv:
			aggregate_csv[stock2pull].append(row)

		for cell in aggregate_csv[stock2pull]:
			if 'values:Date' not in cell:
				for num in range(1, 6):
					cell[num] = float(cell[num])
			else:
				cell[0] = 'Dates'

def export_to_csv(stock2push):
	file_location_csv = str(stock2push) + '.csv'
	with open(file_location_csv, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',')
		for row in aggregate_csv[str(stock2pull)]:
			writer.writerow(row)

def pandas_read_csv(stock2read):
	file_location_csv = str(stock2read) + '.csv'
	df = pd.read_csv(file_location_csv, index_col = 'Dates', parse_dates = True)
	print df.head()
	df[['close', 'high', 'low', 'open']].plot()
	plt.show()

stock2pull = raw_input('Please input the stock name: ')
timespan = raw_input('Please input the timespan(2y for 2 years, 10d for 10 days): ')
pulldata(stock2pull, timespan)

aggregate_csv[str(stock2pull)] = []
if 'y' in timespan:
	import_from_csv_y(stock2pull)
elif 'd' in timespan:
	import_from_csv_d(stock2pull)

stock2push = raw_input('Name a file to import the data: ')
export_to_csv(stock2push)

stock2read = raw_input('Stock2read: ')
pandas_read_csv(stock2read)





