myaccount = 100000
amountinstocks = 0

def buystock(liquidcash, amounttobuy, amountinstocks):
    if amounttobuy > liquidcash:
        print("You don't have enough money to buy", amounttobuy, "stocks")
    else:
        liquidcash = liquidcash - amounttobuy
        amountinstocks = amountinstocks + amounttobuy
        print("you now have", liquidcash, "in your account and", amountinstocks,
              "in stocks")
    return [liquidcash, amountinstocks]




def sellstock(liquidcash, amounttosell, amountinstocks):
    if amounttosell > amountinstocks:
              print("You don't have enough in the market to sell", amounttosell)
    else:
        amountinstocks -= amounttosell
        liquidcash += amounttosell
        print("you now have", liquidcash, "in your account and", amountinstocks, "in stocks")
    return [liquidcash, amountinstocks]


[myaccount, amountinstocks] = buystock(myaccount, 1000, amountinstocks)
[myaccount, amountinstocks] = sellstock(myaccount, 100, amountinstocks)
[myaccount, amountinstocks] = buystock(myaccount, 10000, amountinstocks)
[myaccount, amountinstocks] = buystock(myaccount, 1000, amountinstocks)
