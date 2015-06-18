import numpy

days = 10
list_of_stocks = [0]*10
for i in range(5):
	list_of_stocks[i] = 1
for i in range(5,10):
	list_of_stocks[i] = 4

beta = numpy.std(list_of_stocks)

risk_free = 1
market_rate = 2 

expected_return = risk_free + beta*(market_rate - risk_free)

print("risk free rate", risk_free)
print("std or beta", beta)
print("slope w.r.t. beta", market_rate - risk_free)
print("expected return", expected_return)
print("list_of_stocks", list_of_stocks)