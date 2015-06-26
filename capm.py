import numpy
import matplotlib.pyplot as plt
import bloomberg2dict

my_file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'
#stock_name = raw_input('Tell me the name of the stock: ')
stock_name = 'Default'

my_stock_info = bloomberg2dict.stock2dict(my_file_location_csv, stock_name)

risk_free = int(raw_input('Tell me the risk free rate:' ))
market_rate = int(raw_input('Tell me the market average return: '))
time_to_test = int(raw_input('Tell me the amount of time to test for beta: '))

#days = 10
#beta = 10
range_of_interest = my_stock_info['Default_Close'][0:time_to_test]
beta = numpy.std(range_of_interest)

expected_return = risk_free + beta*(market_rate - risk_free)

print("risk free rate", risk_free)
print("std or beta", beta)
print("slope w.r.t. beta", market_rate - risk_free)
print("expected return", expected_return)
print("list_of_stocks", range_of_interest)
print("std or beta", beta)
print(range_of_interest)

#plt.plot([1, 2, 3, 4])
#plt.ylabel('test')
#plt.show()