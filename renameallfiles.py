import os
import fileinput
for filename in os.listdir("."):

fileindex = 0

while date < last_date:
		date+= delta
		filename = "wsj" + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + "_fileno_"
		dateindex = 0
		filenames = []
		while(os.path.exists(filename + str(dateindex) + ".txt" ):
			os.rename(filename+str(renameindex)+".txt", "wsj_" + fileindex + ".txt" )
			fileindex += 1
			dateindex += 1
			filenames.append("wsj_" + fileindex + ".txt")
		with open('wsjdate' + str(date.year)+ '_' +str(date.month) + '_' + str(date.day) + ".txt", 'w') as fout:
    		for line in fileinput.input(filenames):
        		fout.write(line)
