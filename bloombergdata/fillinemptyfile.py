import os.path
from datetime import datetime, timedelta

first_date = datetime(2010, 1, 1)
delta = timedelta(days=1)
date = first_date
last_date = datetime(2015, 7, 17)
while date < last_date:
	# do things 
	if not (os.path.exists('bloomberg_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day))):
		print ('bloomberg_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day))
		f = open("bloomberg_" + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + ".txt", "w")
		f.write('\n')
		f.close
	date += delta
