list2 = []
open_list = []
close_list = []
pos_m = []
'''
signals = stock_dict[str(stock_name) + '_BSN']
for signal in signals:
	if signal == 'b' or 's':
		list.append([stock_dict[str(stock_name) + '_Close'], signal])
'''
list1 = [[1, 'b'], [2, 'b'], [3, 's'], [4, 's'], [5, 'b'], [6, 'b'], [7, 'b'], [8, 'b'], [9, 's'], [10, 'b'], [11, 's'], [12, 'b'], [13, 's']]

def position(list1):
	if 'b' in list1[0]:
		list2.append(list1[0])
		for record in list1:
			del list1[0]
			if 's' in list1[0]:
				list2.append(list1[0])
				del list1[0]
				break
	elif 's' in list1[0]:
		list2.append(list1[0])
		for record in list1:
			del list1[0]
			if 'b' in list1[0]:
				list2.append(list1[0])
				del list1[0]
				break
	if list1 != []:	
		position(list1)
	return list2

def listsum(numList):
    theSum = 0
    for i in numList:
        theSum = theSum + i
    return theSum

def calculate():
	for pos in range(len(list2)):
		if pos % 2 == 0:
			open_list.append(list2[pos])
		else:
			close_list.append(list2[pos])
	for i in range(len(open_list)):
		if 'b' in open_list[i]:
			pos_m.append(float(- open_list[i][0] + close_list[i][0]))
		else:
			pos_m.append(float(open_list[i][0] - close_list[i][0]))

position(list1)
calculate()
print pos_m
print listsum(pos_m)













