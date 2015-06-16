'''this code generates buy and sell signals based on the historical prices using filter rule
    it takes in a list of lists of date and corresponding stock prices as an argument
    it outputs a list of lists which has buy and sell signals appended to the list of each day
    the signal is represented by a string of a single letter, b=buy, s=sell, n=neither
'''

#listoflists is the original data set containing date and prices, x is the parameter used in the filter rule
#n is the number of days used to determined a local maximum and local minimum of stock prices

def filterRule(listoflists, x, n):
    for i in range(1, n+1):
        listoflists[i].append("n")  #first n days are used to determine the local min/max, so no signal can be produced on these days
    reference=[0]*n                   #initialize the list of prices (we call it reference days) from which we get local min/max
    for i in range(n+1,len(listoflists)): #loop through the rest of days
        for j in range(n):          #loop through the reference days to update the reference prices
            reference[j]=listoflists[j+i-n][2]
        minprice=min(reference)       #determine local max/min
        maxprice=max(reference)
        if listoflists[i][2]<maxprice*(1-x/100.0):  #if current close price is lower than x% of max, then sell 
            listoflists[i].append("s")
        elif listoflists[i][2]>minprice*(1+x/100.0):  #if current close price is higher than x% of min, then buy
            listoflists[i].append("b")
        else:  #otherwise do nothing
            listoflists[i].append("n")
        
            
        
    
