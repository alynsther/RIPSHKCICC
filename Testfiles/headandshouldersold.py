'''
This is trying to catch a pattern of some certain algorithm
'''

'''
The shoulder and head 21312
'''

import random
import numpy

l = 1000
s = 50
m = 1500
s_a = 10
b_a = 10

p = 10

stock_data_set = []
transaction = []

def pattern2sell(a , b , c , d , e):
	if a > b and c > b and a < c and d < c and d < e and e < c: 
		return True

def pattern2buy(a , b , c , d , e):
	if a < b and c < b and a > c and d > c and d > e and e > c: 
		return True

def sell(next_price_sell):
	if s >= s_a:
		global l , s , m
		l = l + s_a * next_price_sell
		s = s - s_a
		m = l + s * next_price_sell
		return m

def buy(next_price_buy):
	if l >= b_a * next_price_buy:
		global l , s , m
		l = l - b_a * next_price_buy
		s = s + b_a
		m = l + s * next_price_buy
		return m
	else:
		global l , s , m
		s = s + l / next_price_buy
		l = l - (l / next_price_buy) * next_price_buy
		m = l + s * next_price_buy
		return m

T = raw_input('Please enter the num of trading days: ')

for t in range(int(T)):
	i = random.randint(1,2)
	if i == 1:
		u = numpy.random.normal(loc = 0.1, scale = 0.01, size = None)
		if u >= 0:
			p = p * (u + 1)
	elif i == 2:
		d = numpy.random.normal(loc = 0.1, scale = 0.01, size = None)
		if d >= 0 and d <= 1:
			p = p * (1 - d)
		else:
			print('exploded')
	stock_data_set.append([p , t])


for n in range(len(stock_data_set) - 4):
	if pattern2sell(stock_data_set[n][0] , stock_data_set[n + 1][0] , stock_data_set[n + 2][0] , stock_data_set[n + 3][0] , stock_data_set[n + 4][0]): 
		next_price_sell = stock_data_set[n + 5][0]
		sell_time = stock_data_set[n + 5][1]
		sell_record = sell(next_price_sell)
		transaction.append([sell_record , sell_time , s , 'sell'])
	elif pattern2buy(stock_data_set[n][0] , stock_data_set[n + 1][0] , stock_data_set[n + 2][0] , stock_data_set[n + 3][0] , stock_data_set[n + 4][0]):
		next_price_buy = stock_data_set[n + 5][0]
		buy(next_price_buy)
		buy_time = stock_data_set[n + 5][1]
		buy_record = buy(next_price_buy)
		transaction.append([buy_record , buy_time , s , 'buy'])
print transaction
