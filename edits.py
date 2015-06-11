'''

General buying/selling stocks program

Change the pattern2buy,pattern2sell to change the technical analysis that gives buy or sell signals

Buy, sell, and the rest of the program merely buy/sell stock, update liquid assets and stock assets, keeping track of how money changes

To add: multiple stocks in different companies, different patterns

'''



import random
import numpy


#declare starting point here, including starting account info, starting stocks, how many stocks to buy at a time, etc.

liquid_assets = 1000
current_stocks = 50
stock_sell_amount = 10
stock_buy_amount = 10
stock_price = 10
total_assets = current_stocks*stock_price + liquid_assets
stock_data_set = []
transaction = []


#head and shoulders buy/sell pattern

def pattern2sell(time1 , time2 , time3 , time4 , time5):
	if time1 > time2 and time3 > time2 and time1 < time3 and time4 < time3 and time4 < time5 and time5 < time3: 
		return True

def pattern2buy(time1 , time2 , time3 , time4 , time5):
	if time1 < time2 and time3 < time2 and time1 > time3 and time4 > time3 and time4 > time5 and time5 > time3: 
		return True


#buy and sell algorithms, globally update assets and stock info

def sell(next_price_sell):
	global liquid_assets, current_stocks , total_assets
	if current_stocks >= stock_sell_amount:
		liquid_assets =liquid_assets+ stock_sell_amount * next_price_sell
		current_stocks = current_stocks - stock_sell_amount
		total_assets = liquid_assets+ current_stocks * next_price_sell
		return total_assets

def buy(next_price_buy):
	global liquid_assets , current_stocks , total_assets
	if  liquid_assets >= stock_buy_amount * next_price_buy:
		liquid_assets = liquid_assets - stock_buy_amount * next_price_buy
		current_stocks = current_stocks + stock_buy_amount
		total_assets = liquid_assets + current_stocks * next_price_buy
		return total_assets
	else:
		current_stocks = current_stocks + liquid_assets / next_price_buy
		liquid_assets = liquid_assets - (liquid_assets / next_price_buy) * next_price_buy
		total_assets = liquid_assets + current_stocks * next_price_buy
		return total_assets

#for loop, going through randomly generated stock prices and making trades based off of what we see

T = raw_input('Please enter the num of trading times: ')

for t in range(int(T)):
	i = random.randint(1,2)
	if i == 1:
		u = numpy.random.normal(loc = 0.1, scale = 0.01, size = None)
		if u >= 0:
			stock_price = stock_price * (u + 1)
	elif i == 2:
		d = numpy.random.normal(loc = 0.1, scale = 0.01, size = None)
		if d >= 0 and d <= 1:
			stock_price = stock_price * (1 - d)
		else:
			print('exploded')
	stock_data_set.append([stock_price , t])


for n in range(len(stock_data_set) - 4):
	if pattern2sell(stock_data_set[n][0] , stock_data_set[n + 1][0] , stock_data_set[n + 2][0] , stock_data_set[n + 3][0] , stock_data_set[n + 4][0]): 
		next_price_sell = stock_data_set[n + 5][0]
		sell_time = stock_data_set[n + 5][1]
		sell_record = sell(next_price_sell)
		transaction.append([sell_record , sell_time , current_stocks , 'sell'])
	elif pattern2buy(stock_data_set[n][0] , stock_data_set[n + 1][0] , stock_data_set[n + 2][0] , stock_data_set[n + 3][0] , stock_data_set[n + 4][0]):
		next_price_buy = stock_data_set[n + 5][0]
		buy(next_price_buy)
		buy_time = stock_data_set[n + 5][1]
		buy_record = buy(next_price_buy)
		transaction.append([buy_record , buy_time , current_stocks , 'buy'])
print transaction
