import os
from datetime import *

first_date = datetime(2010, 1, 1)
delta = timedelta(days=1)
date = first_date - delta
last_date = datetime(2015, 7, 17)
while date < last_date:
	date+= delta
	fileindex = 1
	filename = "wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "_fileno_"
	while(os.path.exists(filename + str(fileindex) + ".txt")):
		statinfo = os.stat(filename + str(fileindex) + ".txt")
		if statinfo.st_size < 1000L:
			os.remove(filename + str(fileindex) + ".txt")
			renameindex = fileindex + 1
			while(os.path.exists(filename + str(renameindex) + ".txt")):
				os.rename(filename+str(renameindex)+".txt", filename+str(renameindex-1)+".txt" )
				renameindex +=1
			


		fileindex +=1

	if not (os.path.exists("wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "_fileno_0.txt")):
		f = open("wsj" + str(date.year)+ '_' +str((date.month)) + '_' + str(date.day) + "_fileno_0.txt", "a")
		f.write('\n')
		f.close


