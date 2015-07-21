import os.path
from datetime import datetime, timedelta

first_date = datetime(2010, 1, 1)
delta = timedelta(days=1)
date = first_date
last_date = datetime(2015, 7, 17)
while date < last_date:
	# do things 
	if not (os.path.exists("wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "_fileno_" + str(linkindex) + ".txt"):
		print ('wsj' + str(date.year) + '_' + str(date.month) + '_' + str(date.day))
		f = open("wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "_fileno_" + str(linkindex) + ".txt", "w")
		f.write('\n')
		f.close
		g = open("wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "error" + ".txt", "w")
		g.write('\n')
		g.close
		print ('error on ' + date)
	date += delta
