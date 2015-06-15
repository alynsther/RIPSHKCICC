'''this code generates a series of stock prices using the geometric brownian motion model
   mu is chosen to be 0.1 and sigma is chosen to be 0.005, we may get more information about how to choose them and update this code
   we can see the stock price in each step and also get a list of stock prices
'''
import math
import random
def generateWt(t):
    return random.gauss(0,t**0.5)
'''the t is the time period we want to consider and n is how many intermediate
   prices we want to get, so the time step will be t/n
   eg, if we want to get a daily stock price, we can set t=1,n=365
   and choose mu to be the yearly drift and sigma to be the yearly violatility
'''
def generateSt(t,n,S0):
    stockprices=[]
    stockprices.append(S0)
    mu=0.1
    sigma=0.005
    t=float(t)
    for i in range(1,n+1):
        stockprices.append(stockprices[i-1]*(math.exp((mu-sigma**2/2)*(t/n)+sigma*generateWt(t/n))))
        print "price at the ",i,"th step is",stockprices[i]
    return stockprices
            
