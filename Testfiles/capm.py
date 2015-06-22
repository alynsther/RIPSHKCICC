import numpy
import matplotlib.pyplot as plt
import bloomberg2dict.py as bloomread


file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'
#stock_name = raw_input('Tell me the name of the stock: ')
stock_name = 'Default'
my_stock_info = bloomread.stock2dict(file_location_csv, stock_name)

#days = 10

beta = numpy.std(my_stock_info.values()[1])

risk_free = 1
market_rate = 2 

expected_return = risk_free + beta*(market_rate - risk_free)

print("risk free rate", risk_free)
print("std or beta", beta)
print("slope w.r.t. beta", market_rate - risk_free)
print("expected return", expected_return)
print("list_of_stocks", list_of_stocks)

plt.plot([1, 2, 3, 4])
plt.ylabel('test')
plt.show()