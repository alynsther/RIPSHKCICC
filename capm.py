import numpy
import matplotlib.pyplot as plt
import bloomberg2dict

print("Test0")
my_file_location_csv = raw_input('Tell me the name of the .csv file you want to import: ') + '.csv'
#stock_name = raw_input('Tell me the name of the stock: ')
stock_name = 'Default'

print('Test1')

my_stock_info = bloomberg2dict.stock2dict(my_file_location_csv, stock_name)

print('Test2')

#days = 10
#beta = 10
beta = numpy.std(my_stock_info['Default_Close'])

risk_free = 1
market_rate = 2 

expected_return = risk_free + beta*(market_rate - risk_free)

print("risk free rate", risk_free)
print("std or beta", beta)
print("slope w.r.t. beta", market_rate - risk_free)
print("expected return", expected_return)
print("list_of_stocks", my_stock_info['Default_Close'])
print("std or beta", beta)


#plt.plot([1, 2, 3, 4])
#plt.ylabel('test')
#plt.show()