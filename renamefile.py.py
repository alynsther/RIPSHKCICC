import os
import fileinput
from datetime import *

fileindex = 0
first_date = datetime(2010, 1, 1)
delta = timedelta(days=1)
date = first_date - delta
last_date = datetime(2015, 7, 17)


while date < last_date:
	date+= delta
	filename = "wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "_fileno_"
	dateindex = 0
	filenames = []
	while(os.path.exists(filename + str(dateindex) + ".txt" )):
		os.rename(filename+str(dateindex)+".txt", "wsj_" + str(fileindex) + ".txt" )
		fileindex += 1
		dateindex += 1
		filenames.append("wsj_" + str(fileindex) + ".txt")
	

	print(filenames)
	with open('wsjdate' + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + ".txt", 'w') as outfile:
		for fname in filenames:
    			with open(fname) as infile:
					for line in infile:
						print(line)
						outfile.write(line)
