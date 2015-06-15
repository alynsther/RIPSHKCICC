


#http://wiki.scipy.org/Cookbook/BrownianMotionhttp://wiki.scipy.org/Cookbook/BrownianMotion

import math
from scipy.stats import norm 
# Process parameters

# Initial condition.
x = 0.0 
# Number of iterations to compute.
def listofprices():
# Iterate to compute the steps of the Brownian motion.
# Process parameters
# Initial condition.
	initialprice = 1
#drift and volatility over full time period
	percentagedrift = .05
	percentvolatility = .1
	newprice = initialprice

#number of iterations of a given timestep
	n = 20 
	stockprices = [0]*n
#x is weiner process and always starts at 0
	x = 0.0
	#what portion of a full period is our timestep
	dt = 0.1
	for k in range(n):
		x = x + norm.rvs(scale=percentvolatility**2*dt)
		newprice = newprice*math.exp((percentagedrift - (percentvolatility**2)/2)+percentvolatility*x)	
		#print("Random Weiner Process", x) 
		#print("Stock price", newprice)
		stockprices[k] = newprice
	return stockprices
		

stocklist = listofprices()
print(stocklist)
