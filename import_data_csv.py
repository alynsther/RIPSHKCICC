import csv

aggregate_csv = {}	#Wanted the data to be a dictionary so that when you call the key(the stock name of the stock), the corresponding data will come out

'''
This function imports data from a certain sheet in a csv file
It currently only works for certain col/row format of a .csv file just like the excel version I wrote earlier
but it can be modified to accommodate other formats too
This version assumes that the first column is the time of each update of stock price
and the second column refers to the open price, third column refers to the close price of the stock
It still works if the .csv file isn't in this format, just some modifications on several lines of code would fix it.
'''

def import_from_csv(particular_stock_csv):
	file_location_csv = raw_input('Tell me the directory of the .csv file you want to import: ')	#This is asking the for the location of the file
	with open(str(file_location_csv)) as csvfile:														#Importing the csv file into a variable
		read_csv = csv.reader(csvfile, delimiter = ',')
		for row in read_csv:
																					#Reading each row of .csv and append it
			del(row[0])
			del(row[6])
			del(row[6])

			aggregate_csv[particular_stock_csv].append(row)
			
		del aggregate_csv[particular_stock_csv][-5:]
		del aggregate_csv[particular_stock_csv][0]
		
		for cell in aggregate_csv[particular_stock_csv]:
			for num in range(1, 6):
				cell[num] = float(cell[num])
			

particular_stock_csv = raw_input('Tell me the name of the stock that you want to import: ')			#You can directly input the file name if this program
aggregate_csv[str(particular_stock_csv)] = []														#is stored in the same directory as the .csv file
import_from_csv(particular_stock_csv)
print aggregate_csv 