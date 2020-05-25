# Project: Stonk Options
Investment firms, hedge funds and retail investors use financial models to understand market behavior and make profitable investments. 
A plethora of information is available in the form of historical stock prices and company performance data, which makes them suitable for machine learning algorithms to process.

Our predictive model regression framework builds on well documented Moving Averages, Momentum, and Volume-based technical indicators with an implementation of regularized regression.
Our web app dashboard generates a forecast of individual stock returns and buy/sell signals in a portfolio of equities for a specified time period.
Given a list of high conviction equity investments, our model recommends suitable entry or exit strategies with an optimal payoff structure using market traded derivatives.

## Pre-requisite
1) MySQL Connection
Execute the following SQL scripts:
```
user.sql
tables.sql
procedures.sql
```

2) IEX API Connection
[Documentation](https://iexcloud.io/docs/api/)
```python
env = 'sandbox'
token = 'Tpk_d7aa551ec78a42ef9b7933450b0d29dc' 

env = 'cloud'
token = 'pk_8f217a39af964a708a5981d1f9cfa931'
```

3) Environment Setup
```bash
chmod 755 setup.sh
./setup.sh
```

## Data Parser Usage
Populate database with all stock historical data:
```bash
python3 parser.py max
```

Update last week's stock prices & next 12 month's option data (scheduled cron job):
```bash
python3 parser.py
```

## Data Analyzer Usage

## Dashboard Usage

## License
[MIT License](https://github.com/jk5ho/stonks-options/blob/master/LICENSE)
