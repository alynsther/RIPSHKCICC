'''this code generates a series of stock prices using the geometric brownian motion model
   mu is chosen to be 0.1 and sigma is chosen to be 0.005, we may get more information about how to choose them and update this code
   we can see the stock price in each step and also get a list of stock prices
'''
'''here in this code, I assume the log return of a stock follows a normal distribution
   this is common in modelling stock price. And in order to estimate mu and sigma
   we try to use the unbiased estimator of mean and variance
   we need to have a list of historical prices first in order to do the simulation
'''
import math
import random
def computesigma(historicalPrices): #traditionally, numbers of days should be somewhere between 90 and 180 or the number of days over which we want to do the simulation
    days=len(historicalPrices)
    sum_u=0
    logreturn=[0]*(days-1)
    for i in range(days-1):  #construct a list of log return
        logreturn[i]=math.log(historicalPrices[i+1]/historicalPrices[i])  #calculate each log return 
        sum_u+=logreturn[i]
    average_u=sum_u/(days-1)   # unbiased estimator of mu of the normal distribution
    sum_difference_square=0
    for i in range(len(logreturn)):
        sum_difference_square+=(logreturn[i]-average_u)**2
    v=(sum_difference_square/(len(logreturn)-1))**0.5     #unbiased estimator of the sd of the normal distribution
    sigma=v/((1.0/252)**0.5)  # scale to be the yearly sigma, note that there are usually 252 trading days a year
    return sigma

def computemu(historicalPrices):
    days=len(historicalPrices)
    sum_u=0
    logreturn=[0]*(days-1)
    for i in range(days-1):
        logreturn[i]=math.log(historicalPrices[i+1]/historicalPrices[i])
        sum_u+=logreturn[i]
    average_u=sum_u/(days-1)#unbiased estimator of mu of the normal distribution
    sigma=computesigma(historicalPrices)
    mu=average_u*252+0.5*(sigma**2)  # result comes from ito's calculus
    return mu
    
def generateWt(t):
    return random.gauss(0,t**0.5)  #generate a random variable follows N(0,t)

'''the t is the time period we want to consider and n is how many intermediate
   prices we want to get, so the time step will be t/n
   eg, if we want to get a daily stock price, we can set t=1,n=252 as there are usually 252 trading days a year
   and choose mu to be the yearly drift and sigma to be the yearly violatility
'''
def generateSt(t,n,S0,historicalPrices):
    stockprices=[]    #construct a list of simulated stock prices
    stockprices.append(S0)
    mu=computemu(historicalPrices)#calculate mu from the pre-defined function
    sigma=computesigma(historicalPrices)  #calculate sigma from the pre-defined function
    t=float(t)
    for i in range(1,n+1):
        stockprices.append(stockprices[i-1]*(math.exp((mu-sigma**2/2)*(t/n)+sigma*generateWt(t/n))))
        print "price at the ",i,"th step is",stockprices[i]
    return stockprices
