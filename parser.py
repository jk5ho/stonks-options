import os
import sys 
import requests
import mysql.connector

# IEX API
env = 'sandbox'
token = 'Tpk_d7aa551ec78a42ef9b7933450b0d29dc' 
# env = 'cloud'
# token = 'pk_8f217a39af964a708a5981d1f9cfa931'

# MySQL Database
host="localhost"
user="hobin"
password="rood"
database="project_stonk"

### API Calls
def stocks_prices(env_type, api_token, symbol, ts_range):
    '''Returns stock pricing in time-series range'''
    response = requests.get("https://" + env_type + ".iexapis.com/stable/stock/" + symbol + "/chart/" + ts_range + "?token=" + api_token)
    if(response.status_code != 200):
        raise Exception("BAD STOCKS RESPONSE: ", response.status_code)
    return response.json()

def option_prices(env_type, api_token, symbol, expiration):
    '''Returns option pricing updated that month'''
    if(expiration == None):
        response = requests.get("https://" + env_type + ".iexapis.com/stable/stock/" + symbol + "/options" + "?token=" + api_token)
    else:
        response = requests.get("https://" + env_type + ".iexapis.com/stable/stock/" + symbol + "/options/" + expiration + "?token=" + api_token)
    if(response.status_code != 200):
        raise Exception("BAD OPTIONS RESPONSE: ", response.status_code)
    return response.json()

def technical_indicators(env_type, api_token, symbol, indicator, range):
    '''Returns technical indicators for certain range'''
    response = requests.get("https://" + env_type + ".iexapis.com/stable/stock/" + symbol + "/indicator/" + indicator + "?range=" + range + "&token=" + api_token)
    return response.json()

### Database Calls
def parse_stocks(mydb, mycursor, symbol, entry):   
    '''Parses stock pricing data into MySQL database'''
    # symbol, date, high, low, open, close, volume
    parameters = [symbol, entry['date'], entry['high'], entry['low'], entry['open'], entry['close'], entry['volume']]
    mycursor.callproc("parseStocks", parameters)
    mydb.commit()

def parse_options(mydb, mycursor, entry):
    '''Parses option pricing data into MySQL database'''
    # id, symbol, expiry, contractSize, strikePrice, closingPrice, side, type, volume, openInterest, bid, ask, lastUpdated, isAdjusted
    expiry = entry['expirationDate'][0:4]+"-"+entry['expirationDate'][4:6]+"-"+entry['expirationDate'][6:8]
    side = "put" #TODO
    parameters = [entry['id'], entry['symbol'], expiry, entry['contractSize'], entry['strikePrice'], entry['closingPrice'], side, entry['type'], entry['volume'], entry['openInterest'], entry['bid'], entry['ask'], entry['lastUpdated'], entry['isAdjusted']]
    mycursor.callproc("parseOptions", parameters)
    mydb.commit()

### Helper Functions
def increment_months(year, month):
    if(month == 12): return str(year+1)+"01"
    elif(month >= 9): return str(year)+str(month+1)
    else: return str(year)+"0"+str(month+1)

# response = technical_indicators(env, token, "AAPL", "sma", "6m")
# print(response['indicator'][0])

### Main Method
def main():
    stocks_range = "5d"
    curr = "202005"
    options_range = 12
    
    # UPSTREAM
    mydb = mysql.connector.connect(
        host = host,
        user = user,
        passwd = password,
        database = database
    )
    mycursor = mydb.cursor()

    # Parsing Data to DB
    temp1 = stocks_prices(env, token, "AAPL", stocks_range)
    for item in temp1:
       parse_stocks(mydb, mycursor, "AAPL", item)
    
    for i in range(0,options_range):
        try:
            curr = increment_months(int(curr[0:4]), int(curr[4:6]))
            temp2 = option_prices(env, token, "AAPL", curr)
            for item in temp2:
                parse_options(mydb, mycursor, item)
        except:
            pass

    # DOWNSTREAM
    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
