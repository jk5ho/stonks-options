import os
import sys 
import datetime
import requests
import mysql.connector

from dbconfig import db_config

# IEX API
env = 'sandbox'
token = 'Tpk_d7aa551ec78a42ef9b7933450b0d29dc' 
# env = 'cloud'
# token = 'pk_8f217a39af964a708a5981d1f9cfa931'

### API Calls
def stock_symbols(env_type, api_token):
    '''Returns stock symbols'''
    response = requests.get("https://" + env_type + ".iexapis.com/stable/ref-data/iex/symbols?token=" + api_token)
    if(response.status_code != 200):
        raise Exception("BAD STOCKS RESPONSE: ", response.status_code)
    return response.json()

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
    query = """INSERT IGNORE INTO Stocks (symbol, date, high, low, open, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s) """
    mycursor.executemany(query, entry)
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
    curr = datetime.datetime.today().strftime("%Y%m")
    stocks_range = "5d"
    options_range = 12

    # UPSTREAM
    mydb = mysql.connector.connect(
        host = db_config["host"],
        user = db_config["user"],
        passwd = db_config["password"],
        database = db_config["database"]
    )
    mycursor = mydb.cursor()

    # Parsing API data to DB
    if sys.argv[1] == "max": stocks_range = "max"
    list_symbols = stock_symbols(env, token)
    for symbol in list_symbols:

        # Stock prices
        list_price = stocks_prices(env, token, symbol['symbol'], stocks_range)
        insert_price = []
        for price in list_price:
            insert_records = (symbol['symbol'], price['date'], price['high'], price['low'], price['open'], price['close'], price['volume'])
            insert_price.append(insert_records)
        parse_stocks(mydb, mycursor, symbol['symbol'], insert_price)

        # TODO: Options data
        # mycursor.callproc("cleanOptions")
        # mydb.commit()
        # for i in range(0,options_range):
        #     try:
        #         curr = increment_months(int(curr[0:4]), int(curr[4:6]))
        #         temp2 = option_prices(env, token, symbol['symbol'], curr)
        #         for item in temp2:
        #             parse_options(mydb, mycursor, item)
        #     except:
        #         pass

    # temp3 = technical_indicators(env, token, "AAPL", "sma", "6m")
    # print(temp3['indicator'])

    # DOWNSTREAM
    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
