import random

buy_amount = 10
sell_amount = 10
buy_p = 5
sell_p = 15
current_l = 1000

liquidity = []

def buyorsellstocks(current_p):
	if current_p > sell_p:
		global current_l
		current_l = current_l + sell_amount * current_p
		print(current_l)
	elif current_p < buy_p:
		global current_l
		current_l = current_l - buy_amount * current_p
		print(current_l)
	else:
		print current_l


for time in range(10):
	current_p = random.randint(2,20)
	print(current_p)
	buyorsellstocks(current_p)
	liquidity.append([current_l , int(time) + 1])


