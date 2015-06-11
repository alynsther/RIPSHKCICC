import xlrd

aggregate = {}

'''
This function imports data from a certain sheet in a excel file
It currently only works for certain col/row format of a Excel sheet
but it can be modified to accommodate other formats
This version assumes that the first column is the time of each update of stock price
and the second column refers to the open price, third column refers to the close price of the stock
It still works if the Excel sheet isnt in this format, just some modifications on several lines of code would fix it
'''

def import_from_excel(particular_stock):
	file_location = raw_input('Tell me the directory of the .xls/.xlse file you want to import: ')		#This is asking the for the location of the file
	sheet_index = raw_input('Tell me the exact sheet you want to import: ')								#Using the xlrd module to read the data
	actual_data_set = xlrd.open_workbook(str(file_location))
	sheet = actual_data_set.sheet_by_index(int(sheet_index))
	data = [[sheet.cell_value(row , col) for col in range(sheet.ncols)] for row in range(sheet.nrows)]	#Importing each row into a list
	aggregate[particular_stock]= data																	#Map the stock name to the list of stock price
particular_stock = raw_input('Tell me the name of the stock that you want to input: ')					#Give a name to your stock (like 'AAPL')
aggregate[str(particular_stock)] = []																	#Introducing the content
import_from_excel(particular_stock)
day = raw_input('Which day are you interested: ')														#Check the stock price on a certain day
print aggregate[particular_stock][int(day) - 1]
print aggregate
 