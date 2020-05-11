# Project: Stonk Options

## Pre-requisite
1) MySQL Connection
```python
host = "localhost"
user = "hobin"
password = "rood"
database = "project_stonk"
```

2) IEX API Connection
[Documentation](https://iexcloud.io/docs/api/)
```python
env = 'sandbox'
token = 'Tpk_d7aa551ec78a42ef9b7933450b0d29dc' 

env = 'cloud'
token = 'pk_8f217a39af964a708a5981d1f9cfa931'
```

3) Python - MySQL
```bash
pip3 install mysql-connector-python
```

## Data Parser Usage
Populate database with all stock historical data:
```bash
python3 parser.py all
```

Update last week's stock prices (scheduled cron job):
```bash
python3 parser.py stock
```

Update next 12 month's option data (scheduled cron job):
```bash
python3 parser.py option
```

## Data Analyzer Usage

## Dashboard Usage
