'''this code generates buy and sell signals based on the historical prices using filter rule
    it takes in a list of close prices as an argument
    it outputs a list of signals
    the signal is represented by a string of a single letter, b=buy, s=sell, n=neither
'''

#listofclose is the original data containing closing prices, x is the parameter used in the filter rule
#n is the number of days used to determined a local maximum and local minimum of stock prices

def filterRule(listofclose, x, n):
    listofsignals=[]
    for i in range(n):
        listofsignals.append("n")  #first n days are used to determine the local min/max, so no signal can be produced on these days
    reference=[0]*n                   #initialize the list of prices (we call it reference days) from which we get local min/max
    for i in range(n,len(listofclose)): #loop through the rest of days
        for j in range(n):          #loop through the reference days to update the reference prices
            reference[j]=listofclose[j+i-n]
        minprice=min(reference)       #determine local max/min
        maxprice=max(reference)
        if listofclose[i]<maxprice*(1-x/100.0):  #if current close price is lower than x% of max, then sell 
            listofsignals.append("s")
        elif listofclose[i]>minprice*(1+x/100.0):  #if current close price is higher than x% of min, then buy
            listofsignals.append("b")
        else:  #otherwise do nothing
            listofsignals.append("n")
    return listofsignals
        
            
        
    
