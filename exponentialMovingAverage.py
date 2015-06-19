"""this code modifies the original moving average by using exponential moving average rathen than simple moving average
    a buy signal is given when sma crosses above lma; while a sell signal is given when lma crosses above sma
"""

def calculateEMA(list_of_values, n):    #generate a list of EMA
    ema = []
    alpha = 2.0 / (n + 1)   # forluma alpha=2/(n+1)
    ema.append(list_of_values[0])   #in this calculation first moving average is set to be the first value of the list, (there are also other settings)
    for i in range(1, len(list_of_values)):
        ema.append(list_of_values[i] * alpha+(1 - alpha) * ema[i - 1])  #use formula EMA_toda y =alpha*value_today + (1-alpha) * EMA_yesterday
    return ema

def EMA(listofclose, shortdays, longdays):
    sma = calculateEMA(listofclose, shortdays)  #list of sma
    lma = calculateEMA(listofclose, longdays)   #list of lma
    listofsignals = []
    listofsignals.append("n")
    print sma
    print lma
    for i in range(1,len(listofclose)):
        if sma[i - 1]<lma[i - 1] and sma[i]>lma[i]:  #if sma crosses above lma, then buy
            listofsignals.append("b")
        elif sma[i - 1]>lma[i - 1] and sma[i]<lma[i]:    #if sma crosses below lma, then buy
            listofsignals.append("s")
        else:   #otherwise, do nothing
            listofsignals.append("n")
    return listofsignals
        
