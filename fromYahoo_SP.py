import pandas as pd
from pandas import DataFrame

import datetime
import pandas.io.data 


#Allen's original code
# year_s = int(raw_input('Starting year: '))
# month_s = int(raw_input('Starting month: '))
# day_s = int(raw_input('Starting day: '))

# year_e = int(raw_input('Ending year: '))
# month_e = int(raw_input('Ending month: '))
# day_e = int(raw_input('Ending day: '))

# sp500 = pd.io.data.get_data_yahoo('%5EGSPC', 
# 	start = datetime.datetime(year_s, month_s, day_s), 
# 	end = datetime.datetime(year_e, month_e, day_e))

# print sp500
# print sp500.head()

# sp500.to_csv('sp500.csv')

def mainPd():
	year_s = int(raw_input('Starting year: '))
	month_s = int(raw_input('Starting month: '))
	day_s = int(raw_input('Starting day: '))

	year_e = int(raw_input('Ending year: '))
	month_e = int(raw_input('Ending month: '))
	day_e = int(raw_input('Ending day: '))
        #S&P 500 is %5EGSPC
	sp500 = pd.io.data.get_data_yahoo('%5EGSPC', 
	start = datetime.datetime(year_s, month_s, day_s), 
	end = datetime.datetime(year_e, month_e, day_e))

	print sp500
	print sp500.head()

	sp500.to_csv('sp500.csv')
