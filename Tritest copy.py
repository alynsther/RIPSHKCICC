from __future__ import division

import random
import decimal

current_s = 50
buy_amount = 10
sell_amount = 10
buy_p = 9.5
sell_p = 10.5
current_l = 1000
current_t = 1000
ar = 0

liquidity = []

T = 20 #Total time span
dt = 1 #time step
current_p = 10 #initial stock price
u = 1.1 #stock price goes up 10%
d = 0.9 #stock price goes down 10%
l = 1 #stock price doesn't change

def buyorsellstocks(current_p):
	if current_p > sell_p and current_s >= sell_amount:
		global current_l , current_s , current_t
		current_l = current_l + sell_amount * current_p
		current_s = current_s - sell_amount
		current_t = current_l + current_s * current_p
		print('Your current amount of stock is' , current_s)
		print('Liquidity' , current_l , 'and Total amount', current_t)
	elif current_p < buy_p and current_l > sell_amount * current_p:
		global current_l , current_s , current_t
		current_l = current_l - buy_amount * current_p
		current_s = current_s + sell_amount
		current_t = current_l + current_s * current_p
		print('Your current amount of stock is' , current_s)
		print('Liquidity' , current_l , 'and Total amount', current_t)
	else:
		print('Your current amount of stock is' , current_s)
		print('Liquidity' , current_l , 'and Total amount', current_l + current_s * current_p)
	global ar
	ar = ((current_t - 1500) / 1500)

def comparison(ar):
	mrvalue = current_p * 100 + random.randint(400 , 600)
	mr = (mrvalue - 1500) / 1500.0
	print('The market return is' , mrvalue)
	print('The market return rate is' , mr)
	global cr
	cr = ((ar / mr) * 100) // 1 
	print('The algorithm return rate is', ar, 'The comparison of return rate is' , cr,'%')



for time in range(T):
	i = random.randint(1,3)
	if i == 1:
		global current_p
		current_p = current_p * u
	elif i == 3:
		global current_p
		current_p = current_p * d
	print('-----The stock price is now', current_p)
	buyorsellstocks(current_p)
	comparison(ar)
	liquidity.append([current_l , int(time) + 1])


	

